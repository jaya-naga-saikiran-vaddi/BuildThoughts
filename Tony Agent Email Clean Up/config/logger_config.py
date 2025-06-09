import logging
import os
import sys

LOG_DIR = "logs"
LOG_FILE = "tony_ai_cleaner.log"


def setup_logger(name: str) -> logging.Logger:
    os.makedirs(LOG_DIR, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s: %(message)s')

    fh = logging.FileHandler(os.path.join(LOG_DIR, LOG_FILE), encoding='utf-8')
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
   

    if not logger.handlers:
        logger.addHandler(fh)
     

    return logger
