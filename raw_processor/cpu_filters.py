import cv2
import numpy as np

def apply_all_filters_cpu(image_np):
    denoised_image = cv2.bilateralFilter(image_np, 9, 75, 75)

    lab = cv2.cvtColor(denoised_image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_clahe = clahe.apply(l)
    
    lab_enhanced = cv2.merge((l_clahe, a, b))
    contrast_enhanced_image = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)
    
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    final_image = cv2.filter2D(src=contrast_enhanced_image, ddepth=-1, kernel=sharpen_kernel)
    
    return final_image