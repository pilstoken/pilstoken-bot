from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters,
    RegexHandler
)
import logging
import os
import random
from dotenv import load_dotenv
import time
import datetime
import text2png
import re
import csv

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TELEGRAM_API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN")
LAUNCH_HOUR = os.environ.get("LAUNCH_HOUR")
URL = "pils.finance"
BEER_EMOJI = u'\U0001F37A'
ARROW_RIGHT = u'\U000027A1'


def start_command(update: Update, context: CallbackContext) -> None:
    msg = update.message

    msg.reply_text("Cheers!")


def url_command(update: Update, context: CallbackContext) -> None:
    msg = update.message

    msg.reply_text(get_website_markdown(), parse_mode='MarkdownV2')


def website_command(update: Update, context: CallbackContext) -> None:
    msg = update.message

    msg.reply_text(get_website_markdown(), parse_mode='MarkdownV2')


def socials_command(update: Update, context: CallbackContext) -> None:
    msg = update.message

    msg.reply_photo(open("socials.jpg", 'rb'), caption=get_socials_markdown(), parse_mode='MarkdownV2')


def get_socials_markdown():
    beer_emoji = u'\U0001F37A'

    text = beer_emoji + " *PilsToken Socials* " + beer_emoji + "\n\n"
    text = text + "*Twitter:* [@PilsToken](https://twitter.com/PilsToken)\n"
    text = text + "*Github:* [/pilstoken](https://github.com/pilstoken)\n"
    text = text + "*Telegram:* [@pilstoken](https://t.me/pilstoken)\n"
    text = text + "*Youtube:* [PilsToken](https://www.youtube.com/channel/UCiY3SNLqAZyOW2NvP1d9mpw)"

    return text


def get_website_markdown():
    beer_emoji = u'\U0001F37A'

    text = beer_emoji + " *website* " + beer_emoji + "\n\n"
    text = text + ARROW_RIGHT + " " + URL

    text = escape_text(text)

    return text


def fact_command(update: Update, context: CallbackContext) -> None:
    msg = update.message

    random_fact = random_line("beer_facts.txt")

    text = BEER_EMOJI + " *Random beer fact* " + BEER_EMOJI + "\n\n"
    text = text + random_fact

    text = escape_text(text)

    msg.reply_text(text, parse_mode='MarkdownV2')


def escape_text(text):
    return text \
        .replace("-", "\-") \
        .replace(".", "\.") \
        .replace("(", "\(") \
        .replace(")", "\)") \
        .replace("<", "\<") \
        .replace(">", "\>") \
        .replace("'", "\'") \
        .replace("!", "\!")


def random_line(file):
    random_lines = random.choice(open(file).readlines())
    return random_lines


def handle_new_chat_members(update: Update, context: CallbackContext):
    msg = update.effective_message
    try:
        time.sleep(3)
        # logging.info("deleting message " + str(msg))
        bot.delete_message(
            chat_id=msg.chat.id,
            message_id=msg.message_id,
        )
    except Exception as ex:
        if 'Message to delete not found' in str(ex):
            logging.error('Failed to delete msg: %s', ex)
            return
        elif "Message can't be deleted" in str(ex):
            logging.error('Failed to delete msg: %s', ex)
            return
        else:
            raise


def when_launch(update: Update, context: CallbackContext):
    msg = update.effective_message

    text = "aunch is planned for May 28th, 8 PM UTC!\n\nSee /countdown for exact launch time!"

    if msg.text is not None:
        if "fair" in msg.text.lower() or "presale" in msg.text.lower():
            text = "Fair l" + text
        else:
            text = "L" + text

    msg.reply_text(text)


def how_launch(update: Update, context: CallbackContext):
    msg = update.effective_message

    msg.reply_text("Fair launch was at May 28th, 8 PM UTC!")


def where_buy(update: Update, context: CallbackContext):
    msg = update.effective_message

    msg.reply_text(
        "You can buy at 🥞 Pancakeswap https://exchange.pancakeswap.finance/#/swap?outputCurrency=0xc136a53348d5af2d104e9252041175bf25783bce")


def chart(update: Update, context: CallbackContext):
    msg = update.effective_message

    msg.reply_text("💩 Chart https://poocoin.app/tokens/0xc136a53348d5af2d104e9252041175bf25783bce")


def liquidity(update: Update, context: CallbackContext):
    msg = update.effective_message

    msg.reply_text(
        "🔒 Liquidity locked https://dxsale.app/app/pages/dxlockview?id=1&add=0xbB6D068D6f8deEa09EA8e530b1e17B43427dAC17&type=lplock&chain=BSC")


def countdown(update: Update, context: CallbackContext):
    msg = update.effective_message

    now = datetime.datetime.now()
    launch = datetime.datetime(2021, 5, 28, int(LAUNCH_HOUR), 00, 00)

    cd = "PilsTokenV2 Launch\nCountdown\n\n %d days\n%d hours\n%d minutes\n%d seconds" % daysHoursMinutesSecondsFromSeconds(
        dateDiffInSeconds(now, launch))

    text2png.text2png(cd, "pils.png", background_color="#fed957")

    # msg.reply_text(cd)
    msg.reply_photo(open("pils.png", 'rb'))


def dateDiffInSeconds(date1, date2):
    timedelta = date2 - date1
    return timedelta.days * 24 * 3600 + timedelta.seconds


def daysHoursMinutesSecondsFromSeconds(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return (days, hours, minutes, seconds)


def shill(update: Update, context: CallbackContext):
    msg = update.effective_message

    msg.reply_text("We have a dedicated marketing team, thank you!\n"
                   "For all other matters, feel free to contact @Mason_PILS or @kai23.")


def admin_dev(update: Update, context: CallbackContext):
    msg = update.effective_message

    msg.reply_text("If you are looking for an admin or dev, feel free to contact @Mason_PILS or @kai23.")


def address(update: Update, context: CallbackContext):
    msg = update.effective_message

    text = "Contract address: *0xc136a53348d5af2d104e9252041175bf25783bce*\n\n"
    text = text + "✅ Verified contract https://bscscan.com/tx/0xc136a53348d5af2d104e9252041175bf25783bce\n\n"
    text = text + "✅ Rugscreen https://www.rugscreen.com/scan/certificate?tokenid=075a3a9ea8"

    text = escape_text(text)

    msg.reply_text(text, parse_mode='MarkdownV2')


def ownership(update: Update, context: CallbackContext):
    msg = update.effective_message

    msg.reply_text("Ownership will be renounced after launch!")


def check_airdrop_address(bsc_address):
    with open('token_holders.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            if row[0].upper() == bsc_address.upper():
                return float(row[1])

    return float(0)


def airdrop(update: Update, context: CallbackContext):
    msg = update.effective_message

    p = re.compile("0x[a-fA-F0-9]{40}")
    result = p.search(msg.text)

    bsc_address = result.group(0)

    text = "The BSC address *" + bsc_address + "* "

    airdrop_amount = check_airdrop_address(bsc_address)

    if airdrop_amount > 0:
        text = text + "will participate in the airdrop and receives *" + str(airdrop_amount) + "* PILSv2 tokens!"
    else:
        text = text + "was no PILSv1 holder and therefore will not participate in the airdrop!"

    msg.reply_text(escape_text(text), parse_mode='MarkdownV2')


def handle_left_chat_member(update: Update, context: CallbackContext):
    msg = update.effective_message
    try:
        time.sleep(3)
        # logging.info("deleting message " + str(msg))
        bot.delete_message(
            chat_id=msg.chat.id,
            message_id=msg.message_id,
        )
    except Exception as ex:
        if 'Message to delete not found' in str(ex):
            logging.error('Failed to delete join message: %s' % ex)
            return
        elif "Message can't be deleted" in str(ex):
            logging.error('Failed to delete msg: %s', ex)
            return
        else:
            raise


if __name__ == '__main__':
    updater = Updater(TELEGRAM_API_TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    bot = dispatcher.get_instance().bot

    # commands
    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(CommandHandler('fact', fact_command))
    dispatcher.add_handler(CommandHandler('url', url_command))
    dispatcher.add_handler(CommandHandler('website', website_command))
    dispatcher.add_handler(CommandHandler('countdown', countdown))
    dispatcher.add_handler(CommandHandler('socials', socials_command))

    # join + leave messages
    dispatcher.add_handler(MessageHandler(
        Filters.status_update.new_chat_members, handle_new_chat_members
    ))
    dispatcher.add_handler(MessageHandler(
        Filters.status_update.left_chat_member, handle_left_chat_member
    ))

    # airdrop info
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'0x[a-fA-F0-9]{40}'), airdrop))

    # wen lunch
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(fair)'), how_launch))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(presale)'), how_launch))

    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(launch)'), when_launch))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(lunch)'), when_launch))

    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(ownership)'), ownership))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(renounce)'), ownership))

    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(where.*buy)'), where_buy))

    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(countdown)'), countdown))

    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(twitter)'), socials_command))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(github)'), socials_command))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(socials)'), socials_command))

    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(shill)'), shill))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(promot)'), shill))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(cms)'), shill))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(reddit)'), shill))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(marketing)'), shill))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(advert)'), shill))

    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(admin)'), admin_dev))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(dev)'), admin_dev))

    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(address)'), address))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(adress)'), address))

    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(website)'), website_command))

    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(chart)'), chart))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(poocoin)'), chart))

    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(liquidity)'), liquidity))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(?i)(lock)'), liquidity))

    updater.start_polling()

    updater.idle()
