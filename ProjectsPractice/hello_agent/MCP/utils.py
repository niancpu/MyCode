import logging
from sys import stderr

logging.basicConfig(
    format="[%(asctime)s] [%(levelname)-7s] [%(filename)-14s:%(lineno)-4d] %(message)s",
    level=logging.DEBUG,
    stream=stderr,
)
log=logging.getLogger()