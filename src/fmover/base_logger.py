import appdirs
import logging
import os
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create log file if it does not exist
# Paste python -c "import appdirs; print(appdirs.user_log_dir('fmover'))" in terminal to get the log directory

log_dir = appdirs.user_log_dir("fmover")
if not os.path.exists(os.path.dirname(log_dir)):
    log_dir = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file = os.path.join(log_dir, "fmover.log")

# Create handlers
file_handler = logging.FileHandler(log_file)
console_handler = logging.StreamHandler(sys.stdout)
file_handler.setLevel(logging.DEBUG)
console_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
file_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_format = logging.Formatter("%(message)s")
file_handler.setFormatter(file_format)
console_handler.setFormatter(console_format)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
