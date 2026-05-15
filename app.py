import os
import random
from flask import Flask, render_template, jsonify
import numpy as np
from PIL import Image

app = Flask(__name__)

IMAGE_FILES = [
    "images/apples.jpeg", 
    "images/raspberry.jpeg", 
    "images/strawberries.png", 
    "images/watermelon.jpg"
]
FRUIT_NAMES = ["apples", "raspberry", "strawberries", "watermelon"]

def compute_full_svd(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Missing file error: Could not find image at path '{image_path}'")

    img_obj = Image.open(image_path).convert('RGB')
    img_array = np.array(img_obj)
    height, width, _ = img_array.shape
    
    svd_data = []
    for channel in range(3):
        channel_matrix = img_array[:, :, channel].astype(float)
        U, s, V = np.linalg.svd(channel_matrix, full_matrices=False)
        
        svd_data.append({
            "U": np.round(U, 4).tolist(),
            "s": np.round(s, 2).tolist(),
            "V": np.round(V, 4).tolist()
        })
        
    return svd_data, height, width

def generate_round_payload():
    rand_int = random.randint(0, len(IMAGE_FILES) - 1)
    chosen_path = IMAGE_FILES[rand_int]
    correct_name = FRUIT_NAMES[rand_int]
    
    svd_matrices, height, width = compute_full_svd(chosen_path)
    return {
        "correct": correct_name,
        "svd_matrices": svd_matrices,
        "img_height": height,
        "img_width": width
    }

@app.route("/")
def index():
    try:
        game = generate_round_payload()
        return render_template(
            'index.html',
            correct=game["correct"],
            svd_matrices_json=jsonify(game["svd_matrices"]).get_data(as_text=True),
            names_list_json=jsonify(FRUIT_NAMES).get_data(as_text=True),
            img_height=game["img_height"],
            img_width=game["img_width"]
        )
    except Exception as e:
        return f"<h3>Backend initialization failed. Error: {str(e)}</h3>", 500

@app.route("/api/new-game")
def new_game():
    try:
        game = generate_round_payload()
        return jsonify(game)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
