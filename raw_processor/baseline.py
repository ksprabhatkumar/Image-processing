# generate_baseline_visual.py
import rawpy
import imageio
import os

# --- CONFIGURATION ---
# IMPORTANT: Put the name of the single RAW file you want to use for the report here.
# This file must be in your 'input_raw_images' folder.
RAW_FILE_TO_PROCESS = "image.ARW"  # <--- CHANGE THIS FILENAME

INPUT_DIRECTORY = "input_raw_images"
OUTPUT_DIRECTORY = "output_png_images" # We'll save the baseline in the same output folder

def generate_visual_baseline():
    """
    Creates a visual representation of the baseline (unprocessed) RAW image.
    It performs only the mandatory demosaicing to create a viewable file,
    but skips all custom quality enhancements.
    """
    raw_path = os.path.join(INPUT_DIRECTORY, RAW_FILE_TO_PROCESS)
    output_path = os.path.join(OUTPUT_DIRECTORY, "baseline_visual.png")

    if not os.path.exists(raw_path):
        print(f"Error: The RAW file '{RAW_FILE_TO_PROCESS}' was not found in the '{INPUT_DIRECTORY}' folder.")
        return

    print(f"Generating visual baseline from '{RAW_FILE_TO_PROCESS}'...")

    with rawpy.imread(raw_path) as raw:
        # We perform ONLY the most basic postprocessing to get a viewable RGB image.
        # NO sharpening, NO contrast adjustments are applied. This is the raw sensor data.
        rgb_image = raw.postprocess(use_camera_wb=True, output_bps=8)
    
    imageio.imwrite(output_path, rgb_image)

    print(f"Success! Baseline visual saved to '{output_path}'")
    print("You can now compare 'baseline_visual.png' with the processed version from main.py")

if __name__ == "__main__":
    generate_visual_baseline()