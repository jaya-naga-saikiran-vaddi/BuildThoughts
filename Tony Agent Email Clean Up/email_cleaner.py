import email
import imaplib
from email.header import decode_header

from config import Constants
from ai_classifier import is_unwanted
from config.logger_config import setup_logger

logger = setup_logger("MainRunner")


def clean_inbox():
    logger.info(" Tony AI agent scanning inbox...")

    try:
        mail = imaplib.IMAP4_SSL(Constants.EMAIL_SERVER, timeout=30)
        mail.login(Constants.EMAIL_USER_NAME, Constants.EMAIL_PASSWORD)

        folder = '"[Gmail]/All Mail"'
        labels = ["Promotions", "Social"]

        status, _ = mail.select(folder)
        if status != "OK":
            logger.info(f"[ERROR] Could not open folder: {folder}")
            return

        for label in labels:
            logger.info(f" Checking label: {label}")
            status, data = mail.search(None, f'X-GM-LABELS {label}')
            if status != "OK":
                logger.info(f"[ERROR] Could not search label {label}: {data}")
                continue

            email_ids = data[0].split()
            logger.info(f" Found {len(email_ids)} emails under {label}")

            for eid in email_ids:
                try:
                    status, msg_data = mail.fetch(eid, "(RFC822)")
                    if status != "OK":
                        continue

                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)

                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8", errors="ignore")

                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode(errors="ignore")
                                break
                    else:
                        body = msg.get_payload(decode=True).decode(errors="ignore")

                    if is_unwanted(subject, body):
                        mail.copy(eid, '"[Gmail]/Trash"')
                        mail.store(eid, '+FLAGS', '\\Deleted')
                        logger.info(f" Moved to Trash: {subject}")
                    else:
                        logger.info(f" Kept: {subject}")

                except Exception as e:
                    logger.info(f"[ERROR] Processing email {eid}: {e}")

            mail.expunge()

        mail.logout()
        logger.info(" Inbox cleaning complete.")

    except Exception as e:
        logger.info(f"[ERROR] Connection/Login failed: {e}")
