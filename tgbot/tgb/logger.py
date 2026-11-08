import logging
from pathlib import Path

# Windows path (local) - Docker ichida ishlashi uchun
import os
if os.getenv('IS_DOCKER', 'false').lower() == 'true':
    BASE_DIR = Path('/app')
else:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "telegram_bot.log"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# Create logger instance
logger = logging.getLogger('telegram_bot')