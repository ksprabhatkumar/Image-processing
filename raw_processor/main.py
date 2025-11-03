# main.py
import os
import glob
import time
import concurrent.futures
from utils import setup_directories
from image_processor import process_raw_to_png, PROCESSOR_TYPE

# --- CONFIGURATION ---
INPUT_DIRECTORY = "input_raw_images"
OUTPUT_DIRECTORY = "output_png_images"
MAX_THREADS = os.cpu_count()

def main():
    """Main function to orchestrate the batch processing and display results."""
    setup_directories(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
    
    raw_extensions = ('*.nef', '*.cr2', '*.arw', '*.dng', '*.orf', '*.raf')
    raw_files = []
    for ext in raw_extensions:
        raw_files.extend(glob.glob(os.path.join(INPUT_DIRECTORY, ext)))
    
    if not raw_files:
        print(f"Error: No RAW files found in '{INPUT_DIRECTORY}'.")
        print("Please add some RAW images and run the script again.")
        return

    print("--- High-Performance RAW Processor ---")
    print(f"Found {len(raw_files)} RAW images to process.")
    print(f"Processing Engine: {PROCESSOR_TYPE}")
    print(f"Starting batch processing with {MAX_THREADS} threads...")
    print("-" * 38)
    
    total_start_time = time.time()
    
    results_list = [] # List to store detailed results for the final summary

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_file = {executor.submit(process_raw_to_png, raw_path, OUTPUT_DIRECTORY): raw_path for raw_path in raw_files}
        
        for future in concurrent.futures.as_completed(future_to_file):
            try:
                # Unpack the new, detailed return values
                file_name, success, error_msg, raw_size, final_size = future.result()
                results_list.append({
                    "filename": file_name,
                    "success": success,
                    "raw_size_mb": raw_size,
                    "final_size_mb": final_size,
                    "error": error_msg
                })
            except Exception as exc:
                failed_file = os.path.basename(future_to_file[future])
                results_list.append({
                    "filename": failed_file, "success": False, "raw_size_mb": 0,
                    "final_size_mb": 0, "error": str(exc)
                })
                print(f"A task for '{failed_file}' generated an unexpected exception: {exc}")

    total_end_time = time.time()

    # --- FINAL SUMMARY ---
    success_count = sum(1 for r in results_list if r['success'])
    failure_count = len(results_list) - success_count
    
    print("-" * 38)
    print("--- BATCH PROCESSING COMPLETE ---")
    print(f"Total time taken: {total_end_time - total_start_time:.2f} seconds.")
    print(f"Successfully processed: {success_count} images.")
    print(f"Failed to process: {failure_count} images.")
    print(f"Output files are located in the '{OUTPUT_DIRECTORY}' folder.")
    
    # --- DETAILED FILE SIZE SUMMARY ---
    if results_list:
        print("-" * 38)
        print("--- File Size Summary ---")
        results_list.sort(key=lambda x: x['filename']) # Sort for consistent order
        
        for result in results_list:
            if result['success']:
                size_change = ((result['final_size_mb'] - result['raw_size_mb']) / result['raw_size_mb']) * 100
                change_str = f"(+{size_change:.1f}%)" if size_change > 0 else f"({size_change:.1f}%)"
                
                print(f"  - {result['filename']:<25} | "
                      f"RAW: {result['raw_size_mb']:>5.2f} MB -> "
                      f"PNG: {result['final_size_mb']:>5.2f} MB {change_str}")
            else:
                print(f"  - {result['filename']:<25} | FAILED. Error: {result['error']}")
    
    print("-" * 38)

if __name__ == "__main__":
    main()