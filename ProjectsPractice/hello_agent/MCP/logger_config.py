import logging
import sys

def logger_config():
    logging.basicConfig(
        format="[%(levelname)s] [%(asctime)s] %(name)s %(message)s",
        level=logging.INFO,
        stream=sys.stderr
    )