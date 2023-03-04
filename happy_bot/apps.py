from django.apps import AppConfig


class HappyBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'happy_bot'

    # def ready(self):
    #     import asyncio
    #     import logging
    #     from happy_bday.settings import TELEGRAM_BOT_TOKEN
    #     from happy_bot.core.bot_dicpatcher.set_dispatcher import dp, Bot
    #
    #     async def start():
    #         logging.basicConfig(level=logging.INFO,
    #                             format='%(asctime)s - [%(levelname)s] - %(name)s - '
    #                                    '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
    #                             )
    #
    #         bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode='HTML')
    #
    #         try:
    #             await dp.start_polling(bot)
    #         finally:
    #             await bot.session.close()
    #
    #     asyncio.run(start())
