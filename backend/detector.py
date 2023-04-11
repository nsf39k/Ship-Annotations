import os
import cv2
import zipfile
import numpy as np
import tensorflow as tf
from utils import crop_image, save_cropped_images


class ShipDetector:
    def __init__(self, model_directory, label_map_path):
        self.model_directory = model_directory
        self.label_map_path = label_map_path
        self.detection_model = self.load_model()

    def load_model(self):
        # Load the saved model
        return tf.saved_model.load(self.model_directory)

    def load_image(self, image_path):
        img = cv2.imread(image_path)
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def get_bounding_boxes(self, image, score_threshold=0.5, iou_threshold=0.5):
        detections = self.detection_model(image[tf.newaxis, ...])

        # Extract bounding boxes, scores, and classes from the detections
        bounding_boxes = detections['detection_boxes'][0].numpy()
        scores = detections['detection_scores'][0].numpy()
        classes = detections['detection_classes'][0].numpy().astype(np.int32)

        # Filter detections by score_threshold
        mask = scores >= score_threshold
        bounding_boxes = bounding_boxes[mask]
        scores = scores[mask]
        classes = classes[mask]

        # Perform non-maximum suppression
        indices = tf.image.non_max_suppression(bounding_boxes, scores, max_output_size=100, iou_threshold=iou_threshold)
        return bounding_boxes[indices.numpy()], classes[indices.numpy()]

    def process_and_download_cropped_images(self, image_path, output_directory, score_threshold=0.5, iou_threshold=0.5):
        image = self.load_image(image_path)
        bounding_boxes, classes = self.get_bounding_boxes(image, score_threshold, iou_threshold)

        cropped_images = crop_image(image, bounding_boxes)
        save_cropped_images(cropped_images, classes, output_directory)

        # Create a zip file of the output_directory and return the path
        zip_file_path = os.path.join(output_directory, "cropped_ships.zip")
        with zipfile.ZipFile(zip_file_path, "w") as zipf:
            for root, _, files in os.walk(output_directory):
                for file in files:
                    if file.endswith(".png"):
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), output_directory))
        return zip_file_path