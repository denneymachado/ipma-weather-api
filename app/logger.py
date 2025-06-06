import logging
from logging.handlers import RotatingFileHandler
import os

log_dir = "data/logs"
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger("ipma")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    filename=os.path.join(log_dir, "requests.log"),
    maxBytes=1_000_000,
    backupCount=5
)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
