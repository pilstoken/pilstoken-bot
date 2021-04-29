from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
)
import logging
import os
import random
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TELEGRAM_API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN")


def start_command(update: Update, context: CallbackContext) -> None:
    msg = update.message

    msg.reply_text("Cheers!")


def fact_command(update: Update, context: CallbackContext) -> None:
    msg = update.message

    random_fact = random_line("beer_facts.txt")

    beer_emoji = u'\U0001F37A'

    text = beer_emoji + " *Random beer fact* " + beer_emoji + "\n\n"
    text = text + random_fact

    text = escape_text(text)

    msg.reply_text(text, parse_mode='MarkdownV2')


def escape_text(text):
    return text \
        .replace("-", "\-") \
        .replace(".", "\.") \
        .replace("(", "\(") \
        .replace(")", "\)") \
        .replace("'", "\'") \
        .replace("!", "\!")


def random_line(file):
    random_lines = random.choice(open(file).readlines())
    return random_lines


if __name__ == '__main__':
    updater = Updater(TELEGRAM_API_TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    bot = dispatcher.get_instance().bot

    # commands
    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(CommandHandler('fact', fact_command))

    updater.start_polling()

    updater.idle()
