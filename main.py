import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def svd_compress(image_path, k):
    # Load image and convert to grayscale (matrix of intensity values)
    img = Image.open(image_path).convert('L')
    A = np.array(img)

    # Perform Singular Value Decomposition
    # U: Left singular vectors, S: Singular values, Vt: Right singular vectors
    U, S, Vt = np.linalg.svd(A, full_matrices=False)

    # Reconstruct image using only the top 'k' components
    # Smaller k = more compression but lower quality
    Ak = U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]
    
    return Ak

# Example usage: Reconstruct with top 50 singular values
compressed_img = svd_compress('your_image.jpg', 50)

plt.imshow(compressed_img, cmap='gray')
plt.title("Compressed Image (k=50)")
plt.show()
Use code with caution.
