from happy_bday.settings import TELEGRAM_BOT_TOKEN
from happy_bot.core.bot_dicpatcher.set_dispatcher import Bot


bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode='HTML')
