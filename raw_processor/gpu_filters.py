# gpu_filters.py
import cv2
import numpy as np

def apply_all_filters_gpu(image_np):
    """
    Applies a sequence of filters to an image using the GPU for acceleration.
    Uploads to GPU once, applies all filters, then downloads once.
    
    Args:
        image_np (np.array): The input image as a NumPy array.

    Returns:
        np.array: The processed image as a NumPy array.
    """
    # Create a GpuMat object to hold the image on the GPU
    gpu_frame = cv2.cuda_GpuMat()
    
    # Upload the NumPy array from CPU RAM to the GPU's VRAM
    gpu_frame.upload(image_np)

    # --- Chain all GPU operations here ---

    # 1. Sharpening Filter on GPU
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]], dtype=np.float32)
    # createLinearFilter is a GPU-specific filter object
    filter2D = cv2.cuda.createLinearFilter(cv2.CV_8UC3, cv2.CV_8UC3, sharpen_kernel)
    gpu_frame = filter2D.apply(gpu_frame)
    
    # 2. Brightness/Contrast Adjustment on GPU
    # cv2.cuda.addWeighted is the GPU-accelerated version of this operation
    # alpha=1.1 (contrast), beta=10 (brightness)
    gpu_frame = cv2.cuda.addWeighted(gpu_frame, 1.1, gpu_frame, 0, 10)

    # --- End of GPU operations ---

    # Download the final processed image from GPU VRAM back to CPU RAM
    processed_image = gpu_frame.download()
    
    return processed_image