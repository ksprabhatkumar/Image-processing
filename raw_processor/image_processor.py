# image_processor.py
import os
import rawpy
import imageio
import threading
import time
from utils import get_size_mb

# Dynamically import the correct filter module based on GPU availability
try:
    from utils import is_gpu_available
    if is_gpu_available():
        from gpu_filters import apply_all_filters_gpu as apply_filters
        PROCESSOR_TYPE = "GPU"
    else:
        from cpu_filters import apply_all_filters_cpu as apply_filters
        PROCESSOR_TYPE = "CPU"
except ImportError:
    from cpu_filters import apply_all_filters_cpu as apply_filters
    PROCESSOR_TYPE = "CPU"

def process_raw_to_png(raw_image_path, output_dir):
    """
    Worker function: Processes a single RAW image file into a quality-controlled JPEG file.
    """
    thread_name = threading.current_thread().name
    file_name = os.path.basename(raw_image_path)
    
    # --- CHANGE 1: Set the output extension to .jpg ---
    output_jpg_path = os.path.join(output_dir, os.path.splitext(file_name)[0] + '.jpg')
    
    raw_size_mb = os.path.getsize(raw_image_path) / (1024 * 1024)

    try:
        start_time = time.time()
        print(f"[{thread_name}] Starting: {file_name} (RAW: {raw_size_mb:.2f} MB) [Using {PROCESSOR_TYPE}]")

        with rawpy.imread(raw_image_path) as raw:
            rgb_image = raw.postprocess(use_camera_wb=True, output_bps=8)
        
        processed_image = apply_filters(rgb_image)
        
        # --- CHANGE 2: Save as JPEG with a quality setting ---
        # The 'quality' parameter is used by the imageio backend (Pillow) for JPEGs.
        # 90 is a great balance between quality and file size.
        print(f"[{thread_name}] Saving {file_name} as JPEG (quality=90)...")
        imageio.imwrite(output_jpg_path, processed_image, quality=90)
        
        end_time = time.time()
        final_size_mb = os.path.getsize(output_jpg_path) / (1024 * 1024)
        
        print(f"[{thread_name}] Finished: {file_name} in {end_time - start_time:.2f}s. "
              f"Output size: {final_size_mb:.2f} MB")
        
        return (file_name, True, None, raw_size_mb, final_size_mb)

    except Exception as e:
        print(f"[{thread_name}] FAILED to process {file_name}. Error: {e}")
        return (file_name, False, str(e), raw_size_mb, 0)