# utils.py
import os
import psutil

def setup_directories(input_dir, output_dir):
    """Ensures that the input and output directories exist."""
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

def get_size_mb(numpy_array):
    """Calculates the in-memory size of a NumPy array in Megabytes."""
    return numpy_array.nbytes / (1024 * 1024)

def check_battery_status(threshold: int):
    """
    Checks the device's battery status to decide if the process can proceed.

    Args:
        threshold (int): The minimum battery percentage required if not plugged in.

    Returns:
        tuple[bool, str]: A tuple containing (can_proceed, user_message).
    """
    battery = psutil.sensors_battery()

    if battery is None:
        return (True, "System Check: No battery detected. Proceeding.")

    if battery.power_plugged:
        return (True, f"System Check: Device is plugged in. Proceeding regardless of battery level ({battery.percent}%).")

    current_percent = battery.percent
    if current_percent < threshold:
        message = (
            f"PROCESS ABORTED: Battery level is critically low ({current_percent}%).\n"
            f"The required minimum is {threshold}% to start this intensive process on battery power."
        )
        return (False, message)
    
    return (True, f"System Check: Battery level is sufficient ({current_percent}%). Proceeding.")