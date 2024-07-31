from flask import Flask, jsonify, render_template, request
import subprocess
import os
import uuid
import cv2
import numpy as np

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
RESULT_FOLDER = 'static/results/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('front.html')



@app.route('/run-script', methods=['POST'])
def run_script():
    if request.method == 'POST':
        image = request.files.get('image')
        if not image:
            return jsonify({'message': 'No image file provided'}), 400

        # Save the uploaded image
        image_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.png")
        image.save(image_path)

        # Prepare the output path for the colorized image
        result_image_path = os.path.join(RESULT_FOLDER, f"{uuid.uuid4()}.png")

        try:
            # Run the Python script with the uploaded image path
            result = subprocess.run(['python', 'cv.py', '-i', image_path, '-o', result_image_path], capture_output=True, text=True)
            
            # Return the paths to the input and colorized images
            return jsonify({'message': 'Image colorized successfully !!', 'input_image': image_path, 'colorized_image': result_image_path})
        except Exception as e:
            return jsonify({'message': str(e)}), 500

@app.route('/transform-image', methods=['POST'])
def transform_image():
    data = request.json
    colorized_image_path = data.get('colorized_image')
    translate_x = float(data.get('translate_x', 0))
    translate_y = float(data.get('translate_y', 0))
    rotate_angle = float(data.get('rotate_angle', 0))

    # Prepare the path for the transformed image
    transformed_image_path = os.path.join(RESULT_FOLDER, f"{uuid.uuid4()}.png")

    try:
        # Apply transformations using OpenCV
        image = cv2.imread(colorized_image_path)

        # Translation
        translation_matrix = np.float32([[1, 0, translate_x], [0, 1, translate_y]])
        translated_image = cv2.warpAffine(image, translation_matrix, (image.shape[1], image.shape[0]))

        # Rotation
        center = (translated_image.shape[1] // 2, translated_image.shape[0] // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, rotate_angle, 1.0)
        rotated_image = cv2.warpAffine(translated_image, rotation_matrix, (image.shape[1], image.shape[0]))

        # Save the transformed image
        cv2.imwrite(transformed_image_path, rotated_image)

        return jsonify({'message': 'Image transformed successfully !!', 'transformed_image': transformed_image_path})
    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

    