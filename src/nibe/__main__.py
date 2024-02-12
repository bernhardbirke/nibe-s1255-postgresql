# from fronius_data_postgresql import FroniusToInflux
import os
import logging


from dev.definitions import ROOT_DIR
from src.nibe.postgresql_tasks import PostgresTasks
from src.nibe.data import NibeToPostgres
from src.nibe.config import Configuration

# instance of Configuration class
config = Configuration()

# instance of PostgresTasks class
client = PostgresTasks()

# initialize logging
loggingFile: str = os.path.join(ROOT_DIR, "nibe_s1255.log")

# config of logging module (DEBUG / INFO / WARNING / ERROR / CRITICAL)
logging.basicConfig(
    level=logging.DEBUG,
    filename=loggingFile,
    encoding="utf-8",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


nibetop = NibeToPostgres(
    config,
    client,
)
nibetop.run()
