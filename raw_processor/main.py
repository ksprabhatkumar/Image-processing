# main.py
import os
import glob
import time
import concurrent.futures
from utils import setup_directories, check_battery_status
from image_processor import process_raw_to_png

# --- CONFIGURATION ---
INPUT_DIRECTORY = "input_raw_images"
# --- CHANGE 1: The output directory is now named for JPG files. ---
OUTPUT_DIRECTORY = "output_jpg_images_postEnhanc"
MAX_THREADS = os.cpu_count()
BATTERY_PERCENTAGE_THRESHOLD = 10

def main():
    """Main function to orchestrate the batch processing."""
    setup_directories(INPUT_DIRECTORY, OUTPUT_DIRECTORY)

    print("--- Pre-flight System Check ---")
    can_proceed, message = check_battery_status(BATTERY_PERCENTAGE_THRESHOLD)
    print(message)
    if not can_proceed:
        print("---------------------------------")
        return 
    print("---------------------------------")
    
    raw_extensions = ('*.nef', '*.cr2', '*.arw', '*.dng', '*.orf', '*.raf')
    raw_files = []
    for ext in raw_extensions:
        raw_files.extend(glob.glob(os.path.join(INPUT_DIRECTORY, ext)))
    
    if not raw_files:
        print(f"Error: No RAW files found in '{INPUT_DIRECTORY}'.")
        return

    print("--- High-Performance RAW Processor ---")
    print(f"Found {len(raw_files)} RAW images to process.")
    print(f"Processing Engine: CPU (Stable Version)") 
    print(f"Starting batch processing with {MAX_THREADS} threads...")
    print("-" * 38)
    
    total_start_time = time.time()
    results_list = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_file = {executor.submit(process_raw_to_png, raw_path, OUTPUT_DIRECTORY): raw_path for raw_path in raw_files}
        
        for future in concurrent.futures.as_completed(future_to_file):
            try:
                file_name, success, error_msg, raw_size, final_size = future.result()
                results_list.append({
                    "filename": file_name, "success": success, "raw_size_mb": raw_size,
                    "final_size_mb": final_size, "error": error_msg
                })
            except Exception as exc:
                failed_file = os.path.basename(future_to_file[future])
                results_list.append({
                    "filename": failed_file, "success": False, "raw_size_mb": 0,
                    "final_size_mb": 0, "error": str(exc)
                })

    total_end_time = time.time()
    success_count = sum(1 for r in results_list if r['success'])
    failure_count = len(results_list) - success_count
    
    print("-" * 38)
    print("--- BATCH PROCESSING COMPLETE ---")
    print(f"Total time taken: {total_end_time - total_start_time:.2f} seconds.")
    print(f"Successfully processed: {success_count} images.")
    print(f"Failed to process: {failure_count} images.")
    
    if results_list:
        print("-" * 38)
        print("--- File Size Summary ---")
        results_list.sort(key=lambda x: x['filename'])
        
        for result in results_list:
            if result['success']:
                size_change = ((result['final_size_mb'] - result['raw_size_mb']) / result['raw_size_mb']) * 100
                change_str = f"(+{size_change:.1f}%)" if size_change > 0 else f"({size_change:.1f}%)"
                # --- CHANGE 2: The report label is now "JPG" for clarity. ---
                print(f"  - {result['filename']:<25} | "
                      f"RAW: {result['raw_size_mb']:>5.2f} MB -> "
                      f"JPG: {result['final_size_mb']:>5.2f} MB {change_str}")
            else:
                print(f"  - {result['filename']:<25} | FAILED. Error: {result['error']}")
    
    print("-" * 38)

if __name__ == "__main__":
    main()