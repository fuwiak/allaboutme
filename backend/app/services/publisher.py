import os, requests, logging, random, datetime as dt, json
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import tempfile
import urllib.request

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

FB_TOKEN = os.getenv("FB_TOKEN")
YT_TOKEN = os.getenv("YOUTUBE_TOKEN")
TT_TOKEN = os.getenv("TIKTOK_TOKEN")
TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TG_CHAT = os.getenv("TG_PUBLIC_CHAT_ID")

def download_video(video_url: str) -> str:
    """Скачивает видео во временный файл."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    try:
        urllib.request.urlretrieve(video_url, temp_file.name)
        logger.info(f"Видео скачано: {temp_file.name}")
        return temp_file.name
    except Exception as e:
        logger.error(f"Ошибка скачивания видео: {e}")
        raise

def _post_telegram(video_url: str, caption: str):
    """Публикация в Telegram канал."""
    try:
        # Check if token is configured
        if not TG_TOKEN:
            logger.error("❌ TELEGRAM_BOT_TOKEN не настроен в .env")
            raise Exception("Telegram bot token not configured. Please add TELEGRAM_BOT_TOKEN to .env file")
        
        if not TG_CHAT:
            logger.error("❌ TG_PUBLIC_CHAT_ID не настроен в .env")
            raise Exception("Telegram chat ID not configured. Please add TG_PUBLIC_CHAT_ID to .env file")
        
        api = f"https://api.telegram.org/bot{TG_TOKEN}/sendVideo"
        
        # Пробуем отправить по URL
        response = requests.post(api, data={
            "chat_id": TG_CHAT,
            "caption": caption,
            "video": video_url,
            "parse_mode": "HTML"
        }, timeout=60)
        
        if response.status_code == 200:
            logger.info("✅ Опубликовано в Telegram")
        else:
            logger.warning(f"Telegram API вернул статус {response.status_code}, пробую загрузить файл")
            
            # Скачиваем и загружаем файлом
            video_file = download_video(video_url)
            with open(video_file, 'rb') as f:
                response = requests.post(api, 
                    data={"chat_id": TG_CHAT, "caption": caption},
                    files={"video": f},
                    timeout=120
                )
                response.raise_for_status()
                logger.info("✅ Опубликовано в Telegram (через файл)")
            
            os.unlink(video_file)
            
    except Exception as e:
        logger.error(f"❌ Ошибка публикации в Telegram: {e}")
        raise

def _post_instagram_reel(video_url: str, caption: str):
    """Публикация в Instagram Reels через Meta Graph API."""
    try:
        # Instagram Graph API требует публикации в 2 этапа
        # 1. Создание контейнера медиа
        page_id = os.getenv("FB_PAGE_ID")
        ig_user_id = os.getenv("IG_USER_ID")
        
        if not all([FB_TOKEN, page_id, ig_user_id]):
            logger.warning("⚠️ Instagram API не настроен (нет токенов)")
            return
        
        # Шаг 1: Создание контейнера
        container_url = f"https://graph.facebook.com/v18.0/{ig_user_id}/media"
        container_params = {
            "video_url": video_url,
                                 "caption": caption,
            "media_type": "REELS",
            "access_token": FB_TOKEN
        }
        
        container_response = requests.post(container_url, data=container_params, timeout=60)
        container_response.raise_for_status()
        container_id = container_response.json()["id"]
        
        # Шаг 2: Публикация
        publish_url = f"https://graph.facebook.com/v18.0/{ig_user_id}/media_publish"
        publish_params = {
            "creation_id": container_id,
            "access_token": FB_TOKEN
        }
        
        publish_response = requests.post(publish_url, data=publish_params, timeout=60)
        publish_response.raise_for_status()
        
        logger.info("✅ Опубликовано в Instagram Reels")
        
    except Exception as e:
        logger.error(f"❌ Ошибка публикации в Instagram: {e}")
        # Не поднимаем исключение, чтобы продолжить публикацию на других платформах

def _post_youtube_short(video_url: str, caption: str):
    """Публикация в YouTube Shorts."""
    try:
        if not YT_TOKEN:
            logger.warning("⚠️ YouTube API не настроен")
            return
        
        # Скачиваем видео
        video_file = download_video(video_url)
        
        # Создаем credentials из токена
        creds = Credentials(token=YT_TOKEN)
        youtube = build('youtube', 'v3', credentials=creds)
        
        # Метаданные
        body = {
            'snippet': {
                'title': caption[:100],  # макс 100 символов
                'description': caption,
                'tags': ['astrology', 'shorts', 'numerology', 'humandesign'],
                'categoryId': '22'  # People & Blogs
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Загрузка видео
        media = MediaFileUpload(video_file, chunksize=-1, resumable=True, mimetype='video/mp4')
        
        request = youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )
        
        response = request.execute()
        logger.info(f"✅ Опубликовано в YouTube Shorts: {response['id']}")
        
        os.unlink(video_file)
        
    except Exception as e:
        logger.error(f"❌ Ошибка публикации в YouTube: {e}")

def _post_tiktok(video_url: str, caption: str):
    """Публикация в TikTok."""
    try:
        if not TT_TOKEN:
            logger.warning("⚠️ TikTok API не настроен")
            return
        
        # TikTok Content Posting API
        video_file = download_video(video_url)
        
        # Инициализация загрузки
        init_url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
        headers = {
            "Authorization": f"Bearer {TT_TOKEN}",
            "Content-Type": "application/json"
        }
        
        init_data = {
            "post_info": {
                "title": caption[:150],
                "privacy_level": "PUBLIC_TO_EVERYONE",
                "disable_duet": False,
                "disable_comment": False,
                "disable_stitch": False,
                "video_cover_timestamp_ms": 1000
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": os.path.getsize(video_file)
            }
        }
        
        init_response = requests.post(init_url, headers=headers, json=init_data, timeout=60)
        init_response.raise_for_status()
        
        upload_url = init_response.json()["data"]["upload_url"]
        
        # Загрузка видео
        with open(video_file, 'rb') as f:
            upload_response = requests.put(upload_url, data=f, timeout=300)
            upload_response.raise_for_status()
        
        logger.info("✅ Опубликовано в TikTok")
        
        os.unlink(video_file)
        
    except Exception as e:
        logger.error(f"❌ Ошибка публикации в TikTok: {e}")

def publish_everywhere(video_url: str, caption: str):
    """Публикует видео на все платформы."""
    logger.info(f"📤 Начинаем публикацию: {caption[:50]}...")
    
    errors = []
    
    # Telegram (основная платформа)
    try:
        _post_telegram(video_url, caption)
    except Exception as e:
        errors.append(f"Telegram: {str(e)}")
    
    # Instagram Reels
    try:
        _post_instagram_reel(video_url, caption)
    except Exception as e:
        errors.append(f"Instagram: {str(e)}")
    
    # YouTube Shorts
    try:
        _post_youtube_short(video_url, caption)
    except Exception as e:
        errors.append(f"YouTube: {str(e)}")
    
    # TikTok
    try:
        _post_tiktok(video_url, caption)
    except Exception as e:
        errors.append(f"TikTok: {str(e)}")
    
    if errors:
        error_msg = "\n".join(errors)
        logger.warning(f"⚠️ Публикация завершена с ошибками:\n{error_msg}")
        
        # Отправляем уведомление об ошибках
        from bot import send_error_notification
        import asyncio
        asyncio.run(send_error_notification(f"⚠️ Ошибки публикации:\n{error_msg}"))
    else:
        logger.info("✅ Публикация успешно завершена на всех платформах")
