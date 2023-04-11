# Ship-Annotations
Internal tool to scan satellite images for ships, classify them based on size, and download their bounding boxes.

## Installation

To set up the project, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/nsf39k/ship-annotations.git
```

2. Create a virtual environment and activate it:
```python3 -m venv venv
source venv/bin/activate
```

3. Install the required packages:
```
pip install -r requirements.txt
```

## Usage

1. Run the Flask application:

```
export FLASK_APP=app.py
flask run
```

2. Open your web browser and go to http://127.0.0.1:5000.

3. Upload a 512x512 resolution satellite image containing ships and click the "Detect Ships" button.

4. The application will process the image, identify ships, categorize them, and generate cropped images with bounding boxes.

5. Download the generated .zip file containing the cropped images.

## License

This project is released under the MIT License.
