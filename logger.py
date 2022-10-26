import logging

# Logging config
logger = logging
date_strftime_format = "%d-%b-%y %H:%M:%S"
logging.basicConfig(filename='/Users/ephraimsiegfried/PycharmProjects/DownloadsMover/moved_files.log', datefmt=date_strftime_format, level=logging.INFO,
                    format='%(asctime)s: %(message)s')