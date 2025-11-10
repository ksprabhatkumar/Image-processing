# cpu_filters.py
import cv2
import numpy as np

def apply_all_filters_cpu(image_np):
    """
    Applies a sequence of enhancement filters to an image using the CPU.
    
    Args:
        image_np (np.array): The input image as a NumPy array.

    Returns:
        np.array: The processed image as a NumPy array.
    """
    # 1. Sharpening Filter to enhance fine details
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened_image = cv2.filter2D(src=image_np, ddepth=-1, kernel=sharpen_kernel)

    # 2. Brightness/Contrast Adjustment to make the image more vibrant
    processed_image = cv2.convertScaleAbs(sharpened_image, alpha=1.1, beta=10)
    
    return processed_image