from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Start bot'
        ),
        BotCommand(
            command='update',
            description='Update key'
        ),
        BotCommand(
            command='read',
            description='Read key'
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())