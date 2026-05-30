import logging
import sys

def get_logger(name:str,stream=sys.stderr)->logging.Logger:
    logging.basicConfig(
        format="[%(levelname)s] [%(asctime)s] %(name)s %(lineno)d:%(message)s",
        level=logging.INFO,
        stream=stream
    )
    logger=logging.getLogger(name)
    return logger

