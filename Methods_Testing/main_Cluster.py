import cv2
import numpy as np
from sklearn.cluster import KMeans

#Too Long Processing Time
def pixelate_image_kmeans(input_path, output_path, block_size=32, n_colors=5):
    """
     Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the pixelated image.
        block_size (int): Size of the square blocks for pixelation.
        n_colors (int): Number of colors to use in K-Means clustering.
    """
    # Read the input image
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"Image at path '{input_path}' could not be loaded.")
    height, width = img.shape[:2]
    pixelated_img = np.zeros_like(img)

    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            block = img[y:y+block_size, x:x+block_size]
            block_reshaped = block.reshape(-1, 3)

            kmeans = KMeans(n_clusters=n_colors, random_state=0, n_init=10)
            labels = kmeans.fit_predict(block_reshaped)
            clustered_colors = kmeans.cluster_centers_.astype(int)

            clustered_block = clustered_colors[labels].reshape(block.shape)
            pixelated_img[y:y+block_size, x:x+block_size] = clustered_block
    cv2.imwrite(output_path, pixelated_img)
    print(f"Pixelated image with K-Means saved to '{output_path}'")

input_image_path = "input.jpg"  
output_image_path = "output_pixelated_kmeans.jpg"  
pixelate_image_kmeans(input_image_path, output_image_path, block_size=32, n_colors=5)

