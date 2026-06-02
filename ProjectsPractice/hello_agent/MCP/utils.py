import logging
import sys

def get_logger(name:str,stream=sys.stderr)->logging.Logger:
    logging.basicConfig(
        format="[%(levelname)s]/t[%(asctime)s]/t%(name)s-%(lineno)d：/t%(message)s",
        level=logging.DEBUG,
        stream=stream
    )
    logger=logging.getLogger(name)
    return logger

