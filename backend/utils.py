import os
import cv2
import numpy as np

def crop_image(image, bounding_boxes):
    cropped_images = []

    for box in bounding_boxes:
        ymin, xmin, ymax, xmax = box
        height, width, _ = image.shape
        ymin, xmin, ymax, xmax = int(ymin * height), int(xmin * width), int(ymax * height), int(xmax * width)
        cropped_images.append(image[ymin:ymax, xmin:xmax])

    return cropped_images

def save_cropped_images(cropped_images, classes, output_directory):
    class_names = {1: "large_ship", 2: "medium_ship", 3: "small_boat"}
    class_counts = {1: 0, 2: 0, 3: 0}

    for i, img in enumerate(cropped_images):
        ship_class = classes[i]
        class_counts[ship_class] += 1
        img_filename = f"{class_names[ship_class]}_{class_counts[ship_class]}.png"
        img_path = os.path.join(output_directory, img_filename)
        cv2.imwrite(img_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))