import logging
import os
from datetime import datetime

def setup_logger():
    # Ensure the 'log' directory exists
    log_directory = "log"
    os.makedirs(log_directory, exist_ok=True)

    # Create a file name based on the current time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = os.path.join(log_directory, f"multiagent_prompt_refinement_{timestamp}.log")

    # Set up the logger
    logger = logging.getLogger("CustomLogger")
    logger.setLevel(logging.INFO)

    # Create a file handler
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)

    # Create a formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)

    return logger

# Example usage
if __name__ == "__main__":
    logger = setup_logger()
    logger.info("This is an informational message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
