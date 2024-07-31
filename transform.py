import cv2
import numpy as np
import argparse
import os

# Argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, required=True, help="path to input image")
ap.add_argument("-o", "--output", type=str, required=True, help="path to save the transformed image")
ap.add_argument("-tx", "--translation_x", type=float, default=0, help="Translation in x direction")
ap.add_argument("-ty", "--translation_y", type=float, default=0, help="Translation in y direction")
ap.add_argument("-r", "--rotation", type=float, default=0, help="Rotation in degrees")
args = vars(ap.parse_args())

# Load the input image
image = cv2.imread(args["image"])

# Apply translation
translation_matrix = np.float32([[1, 0, args["translation_x"]], [0, 1, args["translation_y"]]])
translated_image = cv2.warpAffine(image, translation_matrix, (image.shape[1], image.shape[0]))

# Apply rotation
center = (translated_image.shape[1] // 2, translated_image.shape[0] // 2)
rotation_matrix = cv2.getRotationMatrix2D(center, args["rotation"], 1.0)
rotated_image = cv2.warpAffine(translated_image, rotation_matrix, (translated_image.shape[1], translated_image.shape[0]))

# Save the transformed image
cv2.imwrite(args["output"], rotated_image)
