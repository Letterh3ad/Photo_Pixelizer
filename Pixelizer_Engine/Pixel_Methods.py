import cv2
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt

#Input Path: Path of image to modify
#Output Path: Path of modified image to save


def pixelate_image(input_path, output_path, block_size):
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

def pixelate_image_voronoi(input_path, output_path, num_points):
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"Image at path '{input_path}' could not be loaded.")

    height, width, _ = img.shape
    points = np.random.randint(0, min(height, width), size=(num_points, 2))
    vor = Voronoi(points)

    pixelated_img = np.zeros_like(img)

    for region_index in range(len(vor.regions)):
        region = vor.regions[region_index]
        if not region or -1 in region:
            continue

        polygon = [vor.vertices[i] for i in region]
        polygon = np.array(polygon, dtype=np.int32)

        mask = np.zeros((height, width), dtype=np.uint8)
        cv2.fillPoly(mask, [polygon], 1)

        pixel_values = img[mask == 1]
        if len(pixel_values) > 0:
            average_color = pixel_values.mean(axis=0).astype(np.uint8)
            cv2.fillPoly(pixelated_img, [polygon], average_color.tolist())

    cv2.imwrite(output_path, pixelated_img)


def pixelate_frame_realtime(frame, block_size):
    small = cv2.resize(frame, (block_size, block_size), interpolation=cv2.INTER_LINEAR)
    pixelated_frame = cv2.resize(small, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_NEAREST)
    return pixelated_frame

