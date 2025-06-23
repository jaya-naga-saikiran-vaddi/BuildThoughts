import schedule
import time
from email_cleaner import clean_inbox
from config.logger_config import setup_logger

logger = setup_logger("MainRunner")
if __name__ == "__main__":
    logger.info(" Tony AI Agent Scheduler Started")
    clean_inbox()
    schedule.every().day.at("23:00").do(clean_inbox)

    while True:
        schedule.run_pending()
        time.sleep(60)
