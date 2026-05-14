from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

img = Image.open('bee.jpg')
img = np.mean(img, 2)
def compressImg(image_path, n=10):
    # Load and process image
    img_obj = Image.open(image_path)
    # Convert to grayscale numpy array for SVD
    img_array = np.mean(np.array(img_obj), axis=2) 
    
    # SVD Compression
    U, s, V = np.linalg.svd(img_array)
    S = np.zeros(np.shape(img_array))
    for i in range(0, n):
        S[i,i] = s[i]
    recon_img = U @ S @ V
    
    # Convert back to PIL Image
    # Normalize values between 0-255 and convert to unsigned 8-bit integer
    rescaled = (255.0 / recon_img.max() * (recon_img - recon_img.min())).astype(np.uint8)
    img_final = Image.fromarray(rescaled)
    
    # Save to buffer in memory
    buf = io.BytesIO()
    img_final.save(buf, format="PNG")
    buf.seek(0)
    
    # Encode as base64 string
    img_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    return img_data
