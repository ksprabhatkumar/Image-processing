# utils.py
import os
import cv2

def setup_directories(input_dir, output_dir):
    """Ensures that the input and output directories exist."""
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

def is_gpu_available():
    """Checks if OpenCV has access to a CUDA-enabled GPU."""
    try:
        return cv2.cuda.getCudaEnabledDeviceCount() > 0
    except:
        return False

def get_size_mb(numpy_array):
    """Calculates the in-memory size of a NumPy array in Megabytes."""
    return numpy_array.nbytes / (1024 * 1024)