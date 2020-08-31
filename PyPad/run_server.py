import asyncio
import sys
from logging import INFO, FileHandler, Formatter, getLogger
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(filename="../.myenv"))
local_path = Path(__file__).parent
sys.path.append(local_path.parent.as_posix())

from PyPad.config_man.config_man import start_server  # isort:skip


def configure_logging():
    formatter = Formatter("%(message)s")

    handler = FileHandler("C:/Users/posta/logs/pypad.log")
    handler.setFormatter(formatter)

    logger = getLogger("pypad")
    logger.addHandler(handler)
    logger.setLevel(INFO)
    logger.info("logging set")
    return logger


if __name__ == "__main__":
    log = configure_logging()
    with open("C:/Users/posta/logs/file.txt", "w") as my_file:
        my_file.write("started")
    log.info("starting server")
    asyncio.run(start_server())
    log.info("ending server")
