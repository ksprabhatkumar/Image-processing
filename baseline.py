# baseline.py
import os
import glob
import time
import rawpy
import imageio

 
INPUT_DIRECTORY = "input_raw_images"
 
OUTPUT_DIRECTORY = "output_baseline_images"

def main():
    """
    Baseline implementation: processes all images sequentially in a single thread
    with no enhancement filters applied.
    """
    
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
    
    
    raw_extensions = ('*.nef', '*.cr2', '*.arw', '*.dng', '*.orf', '*.raf')
    raw_files = []
    for ext in raw_extensions:
        raw_files.extend(glob.glob(os.path.join(INPUT_DIRECTORY, ext)))
    
    if not raw_files:
        print(f"Error: No RAW files found in '{INPUT_DIRECTORY}'.")
        return

    print("--- Baseline Sequential Processor ---")
    print(f"Found {len(raw_files)} RAW images to process.")
    print("This will process images one by one with NO enhancement filters.")
    print("-" * 38)
    
 
    total_start_time = time.time()
    
 
    for raw_path in raw_files:
        file_name = os.path.basename(raw_path)
        output_path = os.path.join(OUTPUT_DIRECTORY, os.path.splitext(file_name)[0] + '.jpg')
        
        try:
            print(f"Processing {file_name}...")
            
            with rawpy.imread(raw_path) as raw:
                
                rgb_image = raw.postprocess(use_camera_wb=True, output_bps=8)
            
         
            imageio.imwrite(output_path, rgb_image, quality=95)

        except Exception as e:
            print(f"FAILED to process {file_name}. Error: {e}")

 
    total_end_time = time.time()
    
  
    print("-" * 38)
    print("--- BASELINE PROCESSING COMPLETE ---")
    print(f"Total time taken: {total_end_time - total_start_time:.2f} seconds.")
    print(f"Output files are in the '{OUTPUT_DIRECTORY}' folder.")

if __name__ == "__main__":
    main()