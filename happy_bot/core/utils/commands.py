"""ОСНОВНІ КОМАНДИ"""
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    """
    The set_commands function is a coroutine that sets the list of commands
    that your bot knows about. It should be called after start() and before idle().
    It accepts two arguments: a list of BotCommand objects, and an optional scope.
    The scope argument can be either BotCommandScopeDefault or BotCommandScopePrivate,
    and determines whether the commands are visible to all users (default) or only to you (private).

    :param bot: Bot: Access the bot instance
    :return: A list of BotCommand objects
    """
    commands = [
        BotCommand(
            command='start',
            description='Початок роботи'
        ),
        BotCommand(
            command='help',
            description='Допомога'
        ),
        BotCommand(
            command='auth',
            description='Автентифікація'
        ),
        BotCommand(
            command='off',
            description='Деактивація бота'
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
    # BotCommandScopeDefault() => Команди показуються усім користувачам
