import os
import sys
import logging
from dotenv import load_dotenv
load_dotenv()

logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

log_dir = "logs"
log_filepath = os.path.join(log_dir,"running_logs.log")
os.makedirs(log_dir, exist_ok=True)

log_map = {
    "DEBUG" : logging.DEBUG,
    "INFO" : logging.INFO,
    "ERROR" : logging.ERROR, 
    "WARNING" : logging.WARNING,
    "CRITICAL" : logging.CRITICAL
}
logging.basicConfig(
    level= log_map.get(os.getenv("LOG_LEVEL").upper()),
    format= logging_str,

    handlers=[
        # logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("AndyChatBotLogger")