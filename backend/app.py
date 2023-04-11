import os
import zipfile
import tempfile
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import tensorflow as tf
from PIL import Image
import numpy as np
import io

# Load the pre-trained model
model = tf.keras.models.load_model("model.h5")

app = Flask(__name__)

def process_image(image):
    # Resize the image and convert to array
    img = image.resize((224, 224))
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

@app.route('/api/classify', methods=['POST'])
def classify_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file provided'}), 400

    try:
        img = Image.open(file.stream)
    except Exception as e:
        return jsonify({'error': 'Invalid image'}), 400

    input_data = process_image(img)
    predictions = model.predict(input_data)[0]

    # Process the model output into labels and probabilities
    labels = ['large_ship', 'medium_ship', 'small_boat']
    result = {label: prob for label, prob in zip(labels, predictions)}

    return jsonify(result)

@app.route('/api/crop_and_download', methods=['POST'])
def crop_and_download():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file provided'}), 400

    img = Image.open(file.stream)

    # In real-world applications, you should get bounding boxes from your model.
    # Here, we assume you have a function called "get_bounding_boxes" that receives the image and returns a list of bounding boxes.
    bounding_boxes = get_bounding_boxes(img)

    with tempfile.TemporaryDirectory() as tempdir:
        zip_filename = os.path.join(tempdir, "cropped_ships.zip")

        with zipfile.ZipFile(zip_filename, "w") as zipf:
            for idx, (label, bbox) in enumerate(bounding_boxes):
                cropped_image = img.crop(bbox)
                cropped_filename = f"{label}_{idx}.png"
                cropped_filepath = os.path.join(tempdir, cropped_filename)
                cropped_image.save(cropped_filepath)
                zipf.write(cropped_filepath, arcname=cropped_filename)

        return send_file(zip_filename, mimetype='application/zip', as_attachment=True, attachment_filename='cropped_ships.zip')

if __name__ == '__main__':
    app.run(debug=True)
