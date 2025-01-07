import cv2
import numpy as np

def pixelate_image(input_path, output_path, block_size=8):
    """
    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the pixelated image.
        block_size (int): Size of the square blocks for pixelation.
    """
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"Image at path '{input_path}' could not be loaded.")

    height, width = img.shape[:2]

    pixelated_img = np.zeros_like(img)

    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            block = img[y:y+block_size, x:x+block_size]

            avg_color = block.mean(axis=(0, 1)).astype(int)

            pixelated_img[y:y+block_size, x:x+block_size] = avg_color

    cv2.imwrite(output_path, pixelated_img)
    print(f"Pixelated image saved to '{output_path}'")

input_image_path = "input.jpg"  
output_image_path = "output_pixelated_DimRed.jpg"  
pixelate_image(input_image_path, output_image_path, block_size=32)
