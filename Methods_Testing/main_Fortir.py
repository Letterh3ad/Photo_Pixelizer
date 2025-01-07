import cv2
import numpy as np
import matplotlib.pyplot as plt

def pixelate_image_fourier(input_path, output_path, block_size=64):
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"Image at path '{input_path}' could not be loaded.")

    height, width, _ = img.shape
    pixelated_img = np.zeros_like(img)

    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            block = img[y:y+block_size, x:x+block_size]
            dft = np.fft.fft2(block, axes=(0, 1))
            dft_shift = np.fft.fftshift(dft)
            center_y, center_x = block.shape[0] // 2, block.shape[1] // 2
            radius = block_size // 4
            mask = np.zeros(dft_shift.shape[:2], dtype=np.float32)
            cv2.circle(mask, (center_x, center_y), radius, 1, thickness=-1)
            mask = mask[:, :, np.newaxis]  # Add a channel dimension to match block shape
            dft_shift_filtered = dft_shift * mask
            dft_ishift = np.fft.ifftshift(dft_shift_filtered, axes=(0, 1))
            filtered_block = np.fft.ifft2(dft_ishift, axes=(0, 1)).real
            filtered_block_normalized = np.clip(filtered_block, 0, 255).astype(np.uint8)
            pixelated_img[y:y+block_size, x:x+block_size] = filtered_block_normalized

    cv2.imwrite(output_path, pixelated_img)

input_image_path = "input.jpg"
output_image_path = "output_pixelated_fourier_colored.jpg"
pixelate_image_fourier(input_image_path, output_image_path, block_size=32)
