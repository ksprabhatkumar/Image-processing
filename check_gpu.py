# check_gpu.py
import torch

print(f"--- PyTorch and GPU Compatibility Check ---")
print(f"PyTorch version: {torch.__version__}")

# Check #1: Is CUDA (the technology for NVIDIA GPUs) available to PyTorch?
is_available = torch.cuda.is_available()
print(f"Is CUDA available? -> {is_available}")

if not is_available:
    print("\n[FAIL] PyTorch cannot detect a compatible NVIDIA GPU.")
    print("This means your PyTorch installation is likely a CPU-only version.")
    print("SOLUTION: Re-install PyTorch using the official command from their website for a CUDA version.")
else:
    print("\n[SUCCESS] PyTorch can successfully communicate with your GPU.")
    
    # Check #2: How many GPUs can PyTorch see?
    gpu_count = torch.cuda.device_count()
    print(f"Number of GPUs available: {gpu_count}")

    # Check #3: What is the name of your GPU?
    gpu_name = torch.cuda.get_device_name(0)
    print(f"GPU Name: {gpu_name}")

print("\n--- End of Check ---")