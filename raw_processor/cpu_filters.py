# cpu_filters.py
import cv2
import numpy as np

def apply_all_filters_cpu(image_np):
    """
    Applies an intelligent sequence of enhancement filters to an image using the CPU.
    This pipeline is designed for maximum quality with minimal performance impact.
    
    Args:
        image_np (np.array): The input image as a NumPy array.

    Returns:
        np.array: The processed image as a NumPy array.
    """
    
    # --- STEP 1: Denoise while preserving edges ---
    # We use a bilateral filter to smooth flat areas (reducing noise) without blurring edges.
    # This prepares the image for sharpening and improves JPG compression.
    # Parameters: (image, diameter_of_pixel_neighborhood, sigmaColor, sigmaSpace)
    denoised_image = cv2.bilateralFilter(image_np, 9, 75, 75)

    # --- STEP 2: Enhance Local Contrast with CLAHE ---
    # Convert to LAB color space to apply CLAHE only to the Lightness channel.
    # This prevents unnatural shifts in color.
    lab = cv2.cvtColor(denoised_image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Create a CLAHE object (Contrast Limited Adaptive Histogram Equalization).
    # clipLimit is the threshold for contrast limiting.
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_clahe = clahe.apply(l)
    
    # Merge the CLAHE-enhanced Lightness channel back with the original A and B channels.
    lab_enhanced = cv2.merge((l_clahe, a, b))
    contrast_enhanced_image = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)
    
    # --- STEP 3: Sharpen the clean, enhanced image ---
    # This kernel now enhances the real details without amplifying as much noise.
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    final_image = cv2.filter2D(src=contrast_enhanced_image, ddepth=-1, kernel=sharpen_kernel)

    # Note: We are not applying the simple brightness/contrast from before,
    # as the CLAHE step provides a much superior result.
    
    return final_image