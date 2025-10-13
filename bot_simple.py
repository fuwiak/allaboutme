# bot_simple.py - Упрощенный бот только для уведомлений
from telegram import Bot
import asyncio
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("astro.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Глобальный бот
bot = None

def init_bot():
    """Инициализация бота"""
    global bot
    try:
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if token:
            bot = Bot(token=token)
            logger.info("✅ Telegram бот инициализирован")
            return True
        else:
            logger.warning("⚠️ TELEGRAM_BOT_TOKEN не найден")
            return False
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации бота: {e}")
        return False

async def send_video_notification(video_url, caption, script=""):
    """
    Отправка готового видео в Telegram (только уведомление, без кнопок)
    """
    global bot
    if not bot:
        logger.warning("Бот не инициализирован")
        return False
    
    try:
        chat_id = os.getenv("TG_MOD_CHAT_ID")
        if not chat_id:
            logger.error("TG_MOD_CHAT_ID не настроен")
            return False
        
        # Конвертируем file:// URI в путь к файлу
        video_path = video_url
        if video_url.startswith("file://"):
            video_path = video_url.replace("file://", "")
        
        # Проверяем существование файла
        if not os.path.exists(video_path):
            logger.error(f"Видео файл не найден: {video_path}")
            return False
        
        # Отправляем видео как файл
        with open(video_path, 'rb') as video_file:
            await bot.send_video(
                chat_id=chat_id,
                video=video_file,
                caption=f"🎥 Новое видео готово!\n\n{caption}",
                supports_streaming=True
            )
        
        # Отправляем полный сценарий для справки
        if script:
            await bot.send_message(
                chat_id=chat_id,
                text=f"📝 Сценарий:\n{script}\n\n💡 Управление через веб-интерфейс"
            )
        
        logger.info(f"✅ Видео отправлено в Telegram: {os.path.basename(video_path)}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка отправки видео: {e}")
        return False

async def send_notification(message):
    """
    Отправка простого текстового уведомления
    """
    global bot
    if not bot:
        return False
    
    try:
        chat_id = os.getenv("TG_MOD_CHAT_ID")
        if chat_id:
            await bot.send_message(
                chat_id=chat_id,
                text=message
            )
            return True
    except Exception as e:
        logger.error(f"Ошибка отправки уведомления: {e}")
        return False

async def send_error_notification(message):
    """Отправка уведомления об ошибке"""
    return await send_notification(f"🚨 ОШИБКА:\n{message}")

# Инициализация при импорте
init_bot()


