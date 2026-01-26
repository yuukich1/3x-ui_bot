"""Telegram bot handlers."""

from typing import Optional
from loguru import logger
from aiogram import types
from aiogram.filters.command import Command
from database.crud import UsersRepo
from service.vless_service import VlessService


class BotHandlers:
    """Container for bot command handlers."""
    
    def __init__(self):
        self.users_repo = UsersRepo()
        self.vless_service = VlessService()
    
    async def start(self, message: types.Message) -> None:
        """Handle /start command."""
        try:
            welcome_msg = "Вас привествует бот yuukich1\nТут вы можете получить свой vless ключ"
            await message.answer(welcome_msg)
            await self.users_repo.add_new_users(message.chat.username, message.chat.id)
            logger.info(f"New user: {message.chat.username} ({message.chat.id})")
        except Exception as e:
            logger.error(f"Error in start handler: {e}")
            await message.answer("Произошла ошибка. Попробуйте позже.")
    
    async def help_command(self, message: types.Message) -> None:
        """Handle /help command."""
        help_message = (
            "/vless - получить свой vless\n"
            "/create - создать свой vless ключ\n"
            "/remove - удалить свой vless ключ\n"
            "/online - посмотреть список клиентов которые онлайн"
        )
        await message.answer(help_message)
        logger.debug(f"Help requested by {message.chat.username}")
    
    async def get_vless(self, message: types.Message) -> None:
        """Handle /vless command."""
        try:
            vless_link = await self.vless_service.get_vless_link(message.chat.username)
            if vless_link:
                await message.answer(f"Ваш VLESS ключ:\n\n ```\n{vless_link}\n```", parse_mode='MarkdownV2')
            else:
                await message.answer("У вас нет ни одного профиля. Создайте его с помощью /create")
        except Exception as e:
            logger.error(f"Error getting VLESS link: {e}")
            await message.answer("Произошла ошибка при получении ключа.")
    
    async def create_client(self, message: types.Message) -> None:
        """Handle /create command."""
        try:
            await self.vless_service.create_vless_client(message.chat.username)
            await message.answer("✅ Клиент успешно создан")
            logger.info(f"Client created for {message.chat.username}")
        except Exception as err:
            if "already exists" in str(err):
                await message.answer("⚠️ У вас уже есть активный профиль")
            else:
                logger.error(f"Error creating client: {err}")
                await message.answer("❌ Ошибка при создании клиента. Попробуйте позже.")
    
    async def remove_client(self, message: types.Message) -> None:
        """Handle /remove command."""
        await message.answer("❌ Эта функция еще не реализована")
    
    async def get_online(self, message: types.Message) -> None:
        """Handle /online command."""
        await message.answer("⏳ Функция в разработке")
