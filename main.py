from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import os
from collections import Counter

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def extract_colors(image_np, num_colors=10):
    pixels = image_np.reshape(-1, 3)
    pixel_counts = Counter(map(tuple, pixels))
    most_common_colors = pixel_counts.most_common(num_colors)

    return [{'color': [int(c) for c in color], 'count': int(count)} for color, count in most_common_colors]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']

    if not file:
        print("No file uploaded.")
        return jsonify({"error": "No file uploaded."}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    image = Image.open(filepath)
    image_np = np.array(image.convert('RGB'))

    colors = extract_colors(image_np)

    return jsonify({'colors': colors})


if __name__ == '__main__':
    app.run(debug=True)
