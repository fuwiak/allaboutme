import os, time, requests, json, logging
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

HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY")
HEYGEN_AVATAR_ID = os.getenv("HEYGEN_AVATAR_ID", "")
HEYGEN_TEMPLATE_ID = os.getenv("HEYGEN_TEMPLATE_ID", "")  # Рекомендуется для template-based

# HeyGen работает ЛУЧШЕ с templates, чем с direct generation
USE_TEMPLATE_MODE = bool(HEYGEN_TEMPLATE_ID)

# Настройки видео (можно менять через UI)
VIDEO_CONFIG = {
    "use_avatar": True,  # True = с аватаром, False = только фон
    "background_url": "",  # URL загруженного фона
    "voice": "en-US-Neural2-F",  # Голос
    "duration": 30,  # Длительность видео в секундах
    "dimension": {"width": 1080, "height": 1920}  # Вертикальный формат
}

def update_video_config(use_avatar=None, background_url=None, voice=None, duration=None):
    """Обновление конфигурации видео"""
    global VIDEO_CONFIG
    if use_avatar is not None:
        VIDEO_CONFIG["use_avatar"] = use_avatar
    if background_url is not None:
        VIDEO_CONFIG["background_url"] = background_url
    if voice is not None:
        VIDEO_CONFIG["voice"] = voice
    if duration is not None:
        VIDEO_CONFIG["duration"] = max(15, min(60, int(duration)))  # Ограничиваем 15-60 сек
    logger.info(f"Конфигурация видео обновлена: {VIDEO_CONFIG}")

def submit_to_heygen(script: str) -> str:
    """
    Отправляет текст в HeyGen, возвращает id задачи.
    Поддерживает 2 режима:
    1. Template-based (рекомендуется) - если HEYGEN_TEMPLATE_ID задан
    2. Direct generation - если HEYGEN_TEMPLATE_ID пуст
    """
    
    # Заголовки ТОЧНО как в документации HeyGen
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": HEYGEN_API_KEY
    }
    
    # РЕЖИМ 1: Template-based generation (предпочтительный)
    if USE_TEMPLATE_MODE and HEYGEN_TEMPLATE_ID:
        return _submit_via_template(script, headers)
    
    # РЕЖИМ 2: Direct generation (запасной вариант)
    return _submit_direct(script, headers)


def _submit_via_template(script: str, headers: dict) -> str:
    """Генерация через HeyGen Template (рекомендуемый метод)."""
    
    logger.info(f"📋 Используем Template mode: {HEYGEN_TEMPLATE_ID}")
    
    # Переменные для template
    variables = {
        "LLM_bulletin": {  # стандартное имя text variable
            "name": "LLM_bulletin",
            "type": "text",
            "properties": {"content": script}
        }
    }
    
    # Добавляем voice если настроен
    voice_id = VIDEO_CONFIG.get("voice", "en-US-Neural2-F")
    variables["voice_llm"] = {
        "name": "voice_llm",
        "type": "voice",
        "properties": {"voice_id": voice_id}
    }
    
    payload = {
        "caption": False,
        "title": f"AI24TV-{int(time.time())}",
        "variables": variables
    }
    
    url = f"https://api.heygen.com/v2/template/{HEYGEN_TEMPLATE_ID}/generate"
    
    logger.info(f"🚀 POST {url}")
    logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=60)
        
        logger.info(f"📊 Статус: {r.status_code}")
        logger.debug(f"Ответ: {r.text}")
        
        r.raise_for_status()
        
        response_data = r.json()
        video_id = response_data.get("data", {}).get("video_id")
        
        if not video_id:
            raise ValueError(f"Не получен video_id: {response_data}")
        
        logger.info(f"✅ Template video создан: {video_id}")
        return video_id
        
    except Exception as e:
        logger.error(f"❌ Template generation failed: {e}")
        logger.warning("💡 Попытка fallback на direct generation...")
        return _submit_direct(script, headers)


def _submit_direct(script: str, headers: dict) -> str:
    """Direct video generation (запасной метод, требует валидный Avatar ID)."""
    
    logger.info(f"🎬 Используем Direct generation mode")
    
    # Проверяем наличие Avatar ID
    if not HEYGEN_AVATAR_ID or HEYGEN_AVATAR_ID == "your_avatar_id_here":
        raise RuntimeError(
            "❌ Direct generation требует валидный HEYGEN_AVATAR_ID!\n"
            "Решения:\n"
            "1. Укажите HEYGEN_TEMPLATE_ID в .env (рекомендуется)\n"
            "2. ИЛИ укажите реальный HEYGEN_AVATAR_ID из https://app.heygen.com/avatars"
        )
    
    # Формируем минимальный payload согласно документации
    # ВАЖНО: video_inputs ОБЯЗАТЕЛЕН!
    
    # video_inputs - массив сцен
    video_input = {
        "voice": {
            "type": "text",
            "input_text": script,
            "voice_id": VIDEO_CONFIG.get("voice", "en-US-Neural2-F")
        }
    }
    
    # Если используем аватар
    if VIDEO_CONFIG.get("use_avatar", True):
        video_input["character"] = {
            "type": "avatar",
            "avatar_id": HEYGEN_AVATAR_ID,
            "avatar_style": "normal"
        }
        logger.info(f"Режим: С аватаром ({HEYGEN_AVATAR_ID})")
    else:
        logger.info(f"Режим: Только фон (без аватара)")
    
    # Фон
    if VIDEO_CONFIG.get("background_url"):
        video_input["background"] = {
            "type": "image",
            "url": VIDEO_CONFIG["background_url"]
        }
        logger.info(f"Кастомный фон: {VIDEO_CONFIG['background_url']}")
    elif not VIDEO_CONFIG.get("use_avatar", True):
        video_input["background"] = {
            "type": "color",
            "value": "#1a1a2e"
        }
        logger.info("Цветной фон по умолчанию")
    
    # Базовый payload - согласно примеру из документации
    payload = {
        "video_inputs": [video_input],  # ОБЯЗАТЕЛЬНО!
        "dimension": {
            "width": VIDEO_CONFIG.get("dimension", {}).get("width", 1080),
            "height": VIDEO_CONFIG.get("dimension", {}).get("height", 1920)
        },
        "test": False,
        "caption": False
    }
    
    # Список endpoints для попытки (fallback)
    endpoints_to_try = [
        "https://api.heygen.com/v2/videos",  # Новый CREATE endpoint
        "https://api.heygen.com/v2/video/generate",  # Старый generate
    ]
    
    last_error = None
    
    for url in endpoints_to_try:
        try:
            logger.info(f"Попытка отправки POST-запроса в HeyGen API...")
            logger.info(f"URL: {url}")
            logger.debug(f"Headers: {headers}")
            logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
            
            r = requests.post(url, headers=headers, json=payload, timeout=60)
            
            # Детальное логирование ответа
            logger.info(f"Статус код: {r.status_code}")
            logger.debug(f"Ответ: {r.text}")
            
            # Если 404 - пробуем следующий endpoint
            if r.status_code == 404:
                logger.warning(f"404 для {url}, пробуем следующий endpoint...")
                last_error = f"404 для {url}"
                continue
            
            r.raise_for_status()
            
            response_data = r.json()
            
            # Пробуем разные варианты получения video_id
            video_id = (
                response_data.get("data", {}).get("video_id") or
                response_data.get("video_id") or
                response_data.get("data", {}).get("id")
            )
            
            if not video_id:
                logger.error(f"Полный ответ HeyGen: {json.dumps(response_data, indent=2)}")
                raise ValueError(f"Не получен video_id от HeyGen: {response_data}")
            
            logger.info(f"✅ Видео поставлено в очередь: {video_id}")
            logger.info(f"✅ Успешно использован endpoint: {url}")
            
            return video_id
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"Ошибка для {url}: {e}")
            last_error = e
            continue
    
    # Если все endpoints не сработали
    error_msg = f"Все endpoints не сработали. Последняя ошибка: {last_error}"
    logger.error(error_msg)
    
    # Отправляем уведомление об ошибке
    try:
        from bot_simple import send_error_notification
        import asyncio
        
        # Пытаемся получить текущий event loop, если нет - создаем новый
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Запускаем в фоновом режиме, не блокируя основной код
        asyncio.create_task(send_error_notification(f"❌ Ошибка HeyGen: {error_msg}"))
    except Exception as ex:
        logger.warning(f"Не удалось отправить уведомление: {ex}")
    
    raise RuntimeError(error_msg)

def wait_video(video_id: str, timeout=900, progress_callback=None) -> str:
    """Ждёт готовности видео и возвращает прямой URL."""
    status_url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"
    
    headers = {
        "X-Api-Key": HEYGEN_API_KEY,
        "Content-Type": "application/json"
    }
    
    logger.info(f"Ожидание рендеринга видео {video_id}...")
    
    start_time = time.time()
    check_interval = 10  # проверяем каждые 10 секунд
    
    for iteration in range(timeout // check_interval):
        try:
            r = requests.get(status_url, headers=headers, timeout=30)
            r.raise_for_status()
            
            response = r.json()
            data = response.get("data", {})
            status = data.get("status", "unknown")
            
            elapsed = int(time.time() - start_time)
            logger.info(f"Статус видео [{elapsed}s]: {status}")
            
            # Вызываем callback для UI
            if progress_callback:
                progress_callback(status, elapsed)
            
            if status == "completed":
                video_url = data.get("video_url") or data.get("url")
                if video_url:
                    logger.info(f"✅ Видео готово: {video_url}")
                    return video_url
                else:
                    logger.error(f"❌ Видео завершено, но URL не найден: {data}")
                    raise ValueError("Video completed but no URL provided")
                
            if status == "failed":
                error_msg = data.get("error", "Unknown error")
                logger.error(f"❌ HeyGen сообщил об ошибке: {error_msg}")
                raise RuntimeError(f"HeyGen failed: {error_msg}")
            
            # Продолжаем ждать
            time.sleep(check_interval)
            
        except requests.RequestException as e:
            logger.warning(f"Ошибка запроса статуса (попытка {iteration+1}): {e}")
            time.sleep(check_interval)
            continue
    
    # Timeout
    logger.error(f"❌ Timeout: видео не было готово за {timeout} секунд")
    raise TimeoutError(f"Video {video_id} was not ready in {timeout} seconds")

def render_video(script: str, progress_callback=None) -> str:
    """
    Создает видео из сценария и возвращает URL.
    Пробует HeyGen, при ошибке использует open-source fallback.
    """
    try:
        logger.info("🎬 Начало рендеринга видео")
        
        # Пробуем HeyGen
        try:
            video_id = submit_to_heygen(script)
            video_url = wait_video(video_id, progress_callback=progress_callback)
            logger.info(f"✅ HeyGen видео создано: {video_url}")
            return video_url
        except RuntimeError as heygen_error:
            # Если HeyGen не настроен - используем open-source
            error_msg = str(heygen_error)
            if "HEYGEN_AVATAR_ID" in error_msg or "HEYGEN_TEMPLATE_ID" in error_msg:
                logger.warning(f"⚠️ HeyGen не настроен: {heygen_error}")
                logger.info("🔄 Переключаюсь на open-source генератор...")
                
                # Импортируем и используем open-source
                try:
                    from opensource_video import render_video_opensource
                    video_url = render_video_opensource(script, progress_callback)
                    logger.info(f"✅ Open-source видео создано: {video_url}")
                    return video_url
                except ImportError:
                    logger.error("❌ Модуль opensource_video не найден")
                    logger.info("💡 Установите зависимости: pip install moviepy gtts pillow")
                    raise RuntimeError(
                        "HeyGen не настроен и open-source генератор недоступен.\n"
                        "Решение:\n"
                        "1. Настройте HeyGen (рекомендуется): укажите HEYGEN_TEMPLATE_ID в .env\n"
                        "2. ИЛИ установите: pip install moviepy gtts pillow"
                    )
                except Exception as os_error:
                    logger.error(f"❌ Ошибка open-source генератора: {os_error}")
                    raise RuntimeError(
                        f"HeyGen не настроен и open-source генератор не сработал: {os_error}\n"
                        "Решение: настройте HEYGEN_TEMPLATE_ID в .env"
                    )
            else:
                # Другая ошибка HeyGen - пробрасываем
                raise
        
    except Exception as e:
        logger.error(f"❌ Критическая ошибка рендеринга: {e}")
        raise

# Альтернатива: использование n8n webhook
def render_video_via_n8n(script: str) -> str:
    """Альтернативный метод через n8n webhook."""
    n8n_webhook = os.getenv("N8N_WEBHOOK_URL")
    
    if not n8n_webhook:
        logger.warning("N8N_WEBHOOK_URL не настроен, используем прямой API")
        return render_video(script)
    
    try:
        logger.info("Отправка в n8n...")
        response = requests.post(n8n_webhook, json={"script": script}, timeout=60)
        response.raise_for_status()
        
        # Предполагаем, что n8n возвращает video_url
        video_url = response.json().get("video_url")
        
        if video_url:
            logger.info(f"✅ Видео получено через n8n: {video_url}")
            return video_url
        else:
            raise ValueError("n8n не вернул video_url")
            
    except Exception as e:
        logger.error(f"Ошибка n8n, переключаюсь на прямой API: {e}")
        return render_video(script)
