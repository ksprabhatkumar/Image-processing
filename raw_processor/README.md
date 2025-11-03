# High-Performance RAW Image Processor

This project batch-converts RAW image files to high-quality PNGs using a multi-threaded pipeline with a strong emphasis on GPU acceleration.

## Features

- **Multi-Threaded:** Processes multiple images in parallel for maximum throughput on multi-core CPUs.
- **GPU Accelerated:** Leverages NVIDIA GPUs via OpenCV's CUDA module for filter application, with a seamless fallback to CPU if a compatible GPU is not found.
- **Efficient:** Minimizes CPU-GPU memory transfers by chaining filter operations on the GPU.
- **Robust:** Handles errors on a per-file basis, so one bad file won't stop the entire batch.
- **Organized:** Code is split into logical modules for maintainability.

## Setup

1.  **Prerequisites:**
    - Python 3.8+
    - (Optional but recommended) An NVIDIA GPU with CUDA Toolkit and cuDNN installed.

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    Install the required Python packages from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```
    *Note: For GPU support, you might need a specific `opencv-python` build. If the default doesn't work with your CUDA setup, you may need to compile it from source or find a pre-compiled wheel.*

## How to Run

1.  **Place RAW Files:**
    Copy your RAW image files (e.g., `.NEF`, `.CR2`, `.ARW`, `.DNG`) into the `input_raw_images/` directory.

2.  **Execute the Main Script:**
    Run the `main.py` script from the root of the `raw_processor/` directory.
    ```bash
    python main.py
    ```

3.  **Check the Output:**
    The processed PNG files will appear in the `output_png_images/` directory.