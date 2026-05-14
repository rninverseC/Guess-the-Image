from PIL import Image
import numpy as np
import io
import base64

def compressImg(image_path, n):
    # Load and process image
    img_obj = Image.open(image_path)
    img_array = np.array(img_obj)  # Shape: (height, width, 3) for RGB
    
    # Apply SVD to each color channel separately
    compressed_channels = []
    for channel in range(3):  # R, G, B
        channel_data = img_array[:, :, channel].astype(float)
        
        # SVD Compression
        U, s, V = np.linalg.svd(channel_data)
        k = min(channel_data.shape)
        n_components = min(n, k)  # Ensure n doesn't exceed matrix rank
        U_n = U[:, :n_components]
        s_n = s[:n_components]
        V_n = V[:n_components, :]
        recon_channel = U_n @ np.diag(s_n) @ V_n
        
        compressed_channels.append(recon_channel)
    
    # Stack channels back
    recon_img = np.stack(compressed_channels, axis=2)
    
    # Normalize values between 0-255 and convert to unsigned 8-bit integer
    recon_img = np.clip(recon_img, 0, None)  # Ensure non-negative
    rescaled = (255.0 / recon_img.max() * (recon_img - recon_img.min())).astype(np.uint8)
    img_final = Image.fromarray(rescaled)
    
    # Save to buffer in memory
    buf = io.BytesIO()
    img_final.save(buf, format="PNG")
    buf.seek(0)
    
    # Encode as base64 string
    img_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    return img_data
