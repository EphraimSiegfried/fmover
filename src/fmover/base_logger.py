import appdirs
import logging
import os
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create log file if it does not exist
# Paste python -c "import appdirs; print(appdirs.user_log_dir('fmover'))" in terminal to get the log directory
log_path = appdirs.user_log_dir(''.join([appdirs.user_log_dir("fmover"), "/fmover.log"]))
if not os.path.exists(appdirs.user_log_dir("fmover")):
    os.mkdir(appdirs.user_log_dir("fmover"))

# Create handlers
file_handler = logging.FileHandler(log_path)
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



