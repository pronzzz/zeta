import logging
import sys
from rich.logging import RichHandler

def setup_logger(name: str = "zeta", level: str = "INFO"):
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    return logging.getLogger(name)

logger = setup_logger()
