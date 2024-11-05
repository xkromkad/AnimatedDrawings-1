# app.py
from flask import Flask, request, jsonify, send_file
from image_to_annotations import image_to_annotations
from annotations_to_animation import annotations_to_animation
from pathlib import Path
import os
import logging
from flask_cors import CORS
from pkg_resources import resource_filename

app = Flask(__name__)
CORS(app)  # This will allow all origins by defaul

@app.route('/animate', methods=['POST'])
def animate():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 405

    image = request.files['image']
    img_fn = './input_image.png'
    image.save(img_fn)

    char_anno_dir = './output_annotations'
    os.makedirs(char_anno_dir, exist_ok=True)

    # Default configuration files
    motion_cfg_fn = resource_filename(__name__, 'config/motion/dab.yaml')
    retarget_cfg_fn = resource_filename(__name__, 'config/retarget/fair1_ppf.yaml')

    # Generate annotations and animation
    image_to_annotations(img_fn, char_anno_dir)
    output_gif = annotations_to_animation(char_anno_dir, motion_cfg_fn, retarget_cfg_fn)

    # Send the output GIF as a response
    if Path(output_gif).exists():
        return send_file(output_gif, mimetype='image/gif')
    else:
        logging.error("GIF file creation failed or file not found.")
        return jsonify({'error': 'GIF file creation failed or file not found.'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
