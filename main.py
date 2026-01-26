"""3x-UI Telegram Bot - Main Application."""

import asyncio
import logging
from loguru import logger
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config import settings
from database.base import db_manager
from service.handlers import BotHandlers


# Configure logging
logging.basicConfig(level=logging.INFO)
logger.add("bot.log", rotation="500 MB", level="DEBUG")

# Initialize bot and dispatcher
bot = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher()

# Initialize handlers
handlers = BotHandlers()


# Register command handlers
@dp.message(Command('start'))
async def start_handler(message: types.Message):
    """Handle /start command."""
    await handlers.start(message)


@dp.message(Command('help'))
async def help_handler(message: types.Message):
    """Handle /help command."""
    await handlers.help_command(message)


@dp.message(Command('vless'))
async def vless_handler(message: types.Message):
    """Handle /vless command."""
    await handlers.get_vless(message)


@dp.message(Command('create'))
async def create_handler(message: types.Message):
    """Handle /create command."""
    await handlers.create_client(message)


@dp.message(Command('remove'))
async def remove_handler(message: types.Message):
    """Handle /remove command."""
    await handlers.remove_client(message)


@dp.message(Command('online'))
async def online_handler(message: types.Message):
    """Handle /online command."""
    await handlers.get_online(message)


async def main() -> None:
    """Start the bot."""
    logger.info("Starting bot...")
    await db_manager.init_db()
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await db_manager.close()


if __name__ == "__main__":
    asyncio.run(main())
