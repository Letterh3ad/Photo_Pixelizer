import cv2
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt

def pixelate_image_voronoi(input_path, output_path, num_points=500):
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

input_image_path = "input.jpg"
output_image_path = "output_pixelated_voronoi.jpg"
pixelate_image_voronoi(input_image_path, output_image_path, num_points=2000)
