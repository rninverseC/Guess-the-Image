import io
import base64
import numpy as np
from PIL import Image
from flask import Flask, render_template
import matplotlib
matplotlib.use('Agg')  # Prevents server GUI popups
import matplotlib.pyplot as plt

app = Flask(__name__)

def svd_compress(image_path, k):
    # Load image and convert to grayscale
    img = Image.open(image_path).convert('L')
    A = np.array(img)
    
    # Perform Singular Value Decomposition
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    
    # Reconstruct image using only top 'k' components
    Ak = U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]
    return Ak

@app.route('/')
def home():
    # 1. Run your SVD function (replace with your actual image path)
    # Note: Place 'your_image.jpg' in the same main directory as app.py
    try:
        compressed_img = svd_compress('your_image.jpg', 50)
    except FileNotFoundError:
        return "Error: Place 'your_image.jpg' in your project root folder."

    # 2. Plot the compressed numpy matrix using Matplotlib
    plt.figure(figsize=(6, 6))
    plt.imshow(compressed_img, cmap='gray')
    plt.title("Compressed Image (k=50)")
    plt.axis('off')  # Optional: hides the graph X/Y axis pixels

    # 3. Save the plot into the memory buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    plt.close()

    # 4. Encode the image bytes to a web-safe base64 string
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return render_template('index.html', graph_image=plot_data)

if __name__ == '__main__':
    app.run(debug=True)
