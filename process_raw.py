import rawpy
import numpy as np
import cv2
import matplotlib.pyplot as plt

def process_raw_image(image_path):
    """
    Loads a RAW image, processes it, and returns the final image.
    """
    # 1. Loading the RAW image
    with rawpy.imread(image_path) as raw:
        # The postprocess() function handles demosaicing, white balance,
        # and color space conversion with default settings.
        # This gives us a good baseline image to work with.
        rgb_image = raw.postprocess()

    # 2. Basic Image Processing (Gamma Correction)
    # Gamma correction helps adjust the brightness of an image.
    gamma = 2.2  # A standard gamma value
    gamma_corrected_image = np.power(rgb_image / 255.0, 1.0 / gamma)
    gamma_corrected_image = (gamma_corrected_image * 255).astype(np.uint8)

    return gamma_corrected_image

def display_image(image, title="Image"):
    """
    Displays an image using matplotlib.
    """
    plt.imshow(image)
    plt.title(title)
    plt.axis('off')  # Hide axes
    plt.show()

if __name__ == "__main__":
    # Replace 'your_image.raw' with the path to your RAW image file
    raw_image_path = 'image.ARW'

    try:
        # Process the RAW image
        final_image = process_raw_image(raw_image_path)

        # Display the final image
        display_image(final_image, title="Processed RAW Image")

    except FileNotFoundError:
        print(f"Error: The file '{raw_image_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")