import openai
from config import Constants
from config.logger_config import setup_logger

logger = setup_logger("MainRunner")
openai.api_key = Constants.OPENAI_API_KEY


def is_unwanted(subject: str, body: str) -> bool:
#     prompt = f"""
# You're an inbox cleaner. If the email below is either:
# - promotional, marketing, spam, sales, social media notification, or automated update
# - not related to work, personal communication, important bills or subscriptions
#
# Respond only with: true or false
#
# Subject: {subject}
# Body: {body}
# """

    prompt = f"""
    You're an inbox cleaner. If the email below is either:
    - if it is related to Promotions

    Respond only with: true or false

    Subject: {subject}
    Body: {body}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content.strip().lower() == "true"
    except Exception as e:
        logger.info(f"[ERROR] OpenAI API: {e}")
        return False
