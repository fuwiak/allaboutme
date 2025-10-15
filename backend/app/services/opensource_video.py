"""
Open-Source альтернатива HeyGen
Создание видео с фонами (космос, планеты, эзотерика) и AI голосом
Используется когда HeyGen не настроен или как fallback
"""

import os
import logging
import requests
from pathlib import Path
import tempfile

# Ленивый импорт тяжелых библиотек (только когда нужны)
# MoviePy импортируется долго, поэтому импортируем в функциях

# Для улучшенного TTS (опционально)
COQUI_AVAILABLE = False
try:
    from TTS.api import TTS as CoquiTTS
    COQUI_AVAILABLE = True
except ImportError:
    pass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Директория для временных файлов
TEMP_DIR = Path(tempfile.gettempdir()) / "ai24tv"
TEMP_DIR.mkdir(exist_ok=True)

# ElevenLabs API configuration
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY") or os.getenv("ELEVEN_LABS_API_KEY")

# Бесплатные фоны для эзотерических тем
BACKGROUND_URLS = {
    "space": [
        "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=1920&h=1080&fit=crop",  # Млечный путь
        "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1920&h=1080&fit=crop",  # Космос
        "https://images.unsplash.com/photo-1446776653964-20c1d3a81b06?w=1920&h=1080&fit=crop",  # Звезды
    ],
    "planets": [
        "https://images.unsplash.com/photo-1614732414444-096e5f1122d5?w=1920&h=1080&fit=crop",  # Планета
        "https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=1920&h=1080&fit=crop",  # Луна
        "https://images.unsplash.com/photo-1608889825197-79df9699be90?w=1920&h=1080&fit=crop",  # Сатурн
    ],
    "mystical": [
        "https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?w=1920&h=1080&fit=crop",  # Туманность
        "https://images.unsplash.com/photo-1506318137071-a8e063b4bec0?w=1920&h=1080&fit=crop",  # Ночь
        "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1920&h=1080&fit=crop",  # Горы ночью
    ],
    "astrology": [
        "https://images.unsplash.com/photo-1532693322450-2cb5c511067d?w=1920&h=1080&fit=crop",  # Зодиак
        "https://images.unsplash.com/photo-1534796636912-3b95b3ab5986?w=1920&h=1080&fit=crop",  # Звездное небо
        "https://images.unsplash.com/photo-1464802686167-b939a6910659?w=1920&h=1080&fit=crop",  # Звезды крупным планом
    ]
}


def download_background(category: str = "space", index: int = 0) -> Path:
    """Скачать фоновое изображение"""
    try:
        urls = BACKGROUND_URLS.get(category, BACKGROUND_URLS["space"])
        url = urls[index % len(urls)]
        
        bg_file = TEMP_DIR / f"bg_{category}_{index}.jpg"
        
        if bg_file.exists():
            logger.info(f"Фон уже скачан: {bg_file}")
            return bg_file
        
        logger.info(f"Скачиваю фон: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(bg_file, 'wb') as f:
            f.write(response.content)
        
        logger.info(f"✅ Фон сохранен: {bg_file}")
        return bg_file
        
    except Exception as e:
        logger.error(f"Ошибка скачивания фона: {e}")
        # Создаем простой градиентный фон как fallback
        return create_gradient_background()


def create_gradient_background(width: int = 1920, height: int = 1080) -> Path:
    """Создать градиентный фон (fallback)"""
    try:
        from PIL import Image, ImageDraw
        
        bg_file = TEMP_DIR / "bg_gradient.jpg"
        
        # Создаем темно-синий градиент
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        for y in range(height):
            # Градиент от темно-синего к черному
            r = int(10 * (1 - y/height))
            g = int(20 * (1 - y/height))
            b = int(40 * (1 - y/height))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        img.save(bg_file, 'JPEG', quality=85)
        logger.info(f"✅ Создан градиентный фон: {bg_file}")
        return bg_file
        
    except Exception as e:
        logger.error(f"Ошибка создания градиента: {e}")
        raise


def generate_voice_coqui(text: str, lang: str = "ru") -> Path:
    """Генерация голоса через Coqui TTS (высокое качество)"""
    try:
        audio_file = TEMP_DIR / f"voice_coqui_{hash(text)}.wav"
        
        if audio_file.exists():
            logger.info(f"Голос уже сгенерирован: {audio_file}")
            return audio_file
        
        logger.info(f"🎤 Генерирую голос через Coqui TTS ({len(text)} символов)...")
        
        # Используем модель для русского языка
        if lang == "ru":
            model_name = "tts_models/ru/ruslan/tacotron2-DDC"
        else:
            model_name = "tts_models/en/ljspeech/tacotron2-DDC"
        
        tts = CoquiTTS(model_name=model_name, progress_bar=False, gpu=False)
        tts.tts_to_file(text=text, file_path=str(audio_file))
        
        logger.info(f"✅ Голос сохранен (Coqui): {audio_file}")
        return audio_file
        
    except Exception as e:
        logger.warning(f"Ошибка Coqui TTS: {e}, переключаюсь на Google TTS")
        return generate_voice_gtts(text, lang)


def generate_voice_gtts(text: str, lang: str = "ru", slow: bool = False, log_callback=None) -> Path:
    """Генерация голоса через Google TTS (базовое качество)"""
    try:
        from gtts import gTTS
        
        audio_file = TEMP_DIR / f"voice_gtts_{hash(text)}.mp3"
        
        if audio_file.exists():
            logger.info(f"Голос уже сгенерирован: {audio_file}")
            return audio_file
        
        logger.info(f"🎤 Генерирую голос через Google TTS ({len(text)} символов)...")
        
        # Google TTS
        tts = gTTS(text=text, lang=lang, slow=slow)
        tts.save(str(audio_file))
        
        logger.info(f"✅ Голос сохранен (Google): {audio_file}")
        if log_callback:
            log_callback("✅ Голос сохранен (Google)")
        return audio_file
        
    except Exception as e:
        logger.error(f"Ошибка генерации голоса: {e}")
        raise


def generate_voice_elevenlabs(text: str, voice_id: str, log_callback=None) -> Path:
    """Generate voice using ElevenLabs API with selected voice"""
    if not ELEVENLABS_API_KEY:
        logger.warning("⚠️  ELEVENLABS_API_KEY not set, falling back to gTTS")
        if log_callback:
            log_callback("⚠️  ElevenLabs not configured, using gTTS")
        return generate_voice_gtts(text, "ru", False, log_callback)
    
    try:
        logger.info(f"🎙️  Generating audio with ElevenLabs voice: {voice_id}")
        if log_callback:
            log_callback(f"🎙️  Using ElevenLabs voice")
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.5,
                "use_speaker_boost": True
            }
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Save audio
        audio_path = TEMP_DIR / f"elevenlabs_{voice_id[:8]}.mp3"
        with open(audio_path, "wb") as f:
            f.write(response.content)
        
        logger.info(f"✅ ElevenLabs audio generated: {audio_path}")
        if log_callback:
            log_callback(f"✅ Voice generated with ElevenLabs")
        
        return audio_path
        
    except Exception as e:
        logger.error(f"❌ ElevenLabs error: {e}, falling back to gTTS")
        if log_callback:
            log_callback(f"⚠️  ElevenLabs failed, using gTTS")
        return generate_voice_gtts(text, "ru", False, log_callback)


def generate_voice(text: str, lang: str = "ru", slow: bool = False, use_premium: bool = True, log_callback=None) -> Path:
    """
    Генерация голоса - автоматически выбирает лучший доступный движок
    
    Args:
        text: Текст для озвучки
        lang: Язык (ru, en, etc.)
        slow: Медленная речь (только для gTTS)
        use_premium: Использовать Coqui TTS если доступен
    """
    if use_premium and COQUI_AVAILABLE:
        try:
            return generate_voice_coqui(text, lang)
        except Exception as e:
            logger.warning(f"Не удалось использовать Coqui TTS: {e}")
    
    # Fallback на Google TTS
    return generate_voice_gtts(text, lang, slow, log_callback)


def create_opensource_video(
    script: str,
    *,
    background_category: str = "space",
    background_index: int = 0,
    voice_lang: str = "ru",
    voice_slow: bool = False,
    width: int = 1080,
    height: int = 1920,
    add_subtitles: bool = True,
    output_path: Path = None,
    log_callback=None,
    custom_background_path: str = None,
    text_position: str = "center",
    voice_id: str = None
) -> Path:
    """
    Создать видео с open-source инструментами
    
    Args:
        script: Текст сценария
        background_category: Категория фона (space, planets, mystical, astrology)
        background_index: Индекс фона в категории
        voice_lang: Язык голоса (ru, en, etc.)
        custom_background_path: Custom background image path (overrides category)
        text_position: Text position (top, center, bottom)
        voice_id: ElevenLabs voice ID for TTS
        voice_slow: Медленная речь
        width: Ширина видео
        height: Высота видео
        add_subtitles: Добавить субтитры
        output_path: Путь для сохранения
    
    Returns:
        Path к созданному видео
    """
    try:
        # Импортируем MoviePy 2.x (новая структура)
        from moviepy.audio.io.AudioFileClip import AudioFileClip
        from moviepy.video.VideoClip import ImageClip, TextClip
        from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
        
        logger.info(f"🎬 Создание open-source видео...")
        logger.info(f"   Фон: {background_category}")
        logger.info(f"   Скрипт: {len(script)} символов")
        
        # 1. Скачиваем/создаем фон (или используем custom)
        if custom_background_path:
            logger.info(f"🖼️  Custom background requested: {custom_background_path}")
            
            # Convert URL to filesystem path
            if custom_background_path.startswith('/storage/'):
                # URL format: /storage/backgrounds/filename.jpg
                # Convert to: STORAGE_ROOT/backgrounds/filename.jpg
                from .. import storage as storage_module
                if storage_module.STORAGE_ROOT:
                    relative_path = custom_background_path.replace('/storage/', '')
                    bg_path = storage_module.STORAGE_ROOT / relative_path
                    logger.info(f"🔄 Converted URL to path: {bg_path}")
                else:
                    logger.error(f"❌ STORAGE_ROOT not initialized!")
                    bg_path = Path(custom_background_path)
            else:
                # Already a filesystem path
                bg_path = Path(custom_background_path)
            
            if bg_path.exists():
                bg_image = bg_path
                logger.info(f"✅ Using custom background: {bg_image}")
                if log_callback:
                    log_callback(f"✅ Custom background: {bg_image.name}")
            else:
                logger.warning(f"⚠️  Custom background not found at {bg_path}, using default")
                if log_callback:
                    log_callback(f"⚠️  Custom background not found, using default")
                bg_image = download_background(
                    category=background_category,
                    index=background_index
                )
        else:
            logger.info(f"🖼️  Using auto-detected background: {background_category}")
            bg_image = download_background(category=background_category, index=background_index)
            if log_callback:
                log_callback(f"✅ Background category: {background_category}")
        
        # 2. Генерируем голос (с выбранным voice_id если есть)
        if log_callback:
            log_callback(f"🎤 Генерирую голос{f' ({voice_id})' if voice_id else ''}...")
        
        if voice_id:
            # Use ElevenLabs with selected voice
            logger.info(f"🎤 Using ElevenLabs voice: {voice_id}")
            if log_callback:
                log_callback(f"🎤 Voice: ElevenLabs ({voice_id})")
            audio_file = generate_voice_elevenlabs(script, voice_id, log_callback)
        else:
            # Use default (gTTS)
            logger.info(f"🎤 Using default gTTS voice (lang={voice_lang})")
            if log_callback:
                log_callback(f"🎤 Voice: gTTS ({voice_lang})")
            audio_file = generate_voice(script, lang=voice_lang, slow=voice_slow, log_callback=log_callback)
        
        # 3. Загружаем аудио и получаем длительность
        audio_clip = AudioFileClip(str(audio_file))
        duration = audio_clip.duration
        
        logger.info(f"   Длительность аудио: {duration:.1f}с")
        if log_callback:
            log_callback(f"✅ Голос готов! Длительность: {duration:.1f}с")
        
        # 4. Создаем видео клип из фона
        bg_clip = ImageClip(str(bg_image)).with_duration(duration)
        
        # Масштабируем до вертикального формата (1080x1920)
        bg_clip = bg_clip.resized(height=height)
        
        # Обрезаем по центру до нужной ширины
        w, h = bg_clip.size
        x_center = w / 2
        x1 = int(x_center - width / 2)
        x2 = int(x_center + width / 2)
        bg_clip = bg_clip.cropped(x1=x1, x2=x2, y1=0, y2=height)
        
        # 5. Добавляем субтитры если нужно
        clips = [bg_clip]
        
        if add_subtitles:
            try:
                # Разбиваем текст на части для субтитров
                words = script.split()
                words_per_subtitle = 5
                subtitle_duration = duration / (len(words) / words_per_subtitle)
                
                subtitle_clips = []
                for i in range(0, len(words), words_per_subtitle):
                    subtitle_text = " ".join(words[i:i+words_per_subtitle])
                    start_time = i / words_per_subtitle * subtitle_duration
                    
                    txt_clip = TextClip(
                        text=subtitle_text,
                        font_size=40,
                        color='white',
                        font='Arial',
                        stroke_color='black',
                        stroke_width=2,
                        method='caption',
                        size=(width - 100, None)
                    ).with_position(('center', height - 200))
                    
                    txt_clip = txt_clip.with_start(start_time).with_duration(
                        min(subtitle_duration, duration - start_time)
                    )
                    
                    subtitle_clips.append(txt_clip)
                
                # Добавляем субтитры к видео
                clips.extend(subtitle_clips)
                logger.info(f"✅ Добавлено {len(subtitle_clips)} субтитров")
                
            except Exception as e:
                logger.warning(f"Не удалось добавить субтитры: {e}")
        
        # 6. Композитируем финальное видео
        final_clip = CompositeVideoClip(clips, size=(width, height))
        final_clip = final_clip.with_audio(audio_clip)
        
        # 7. Сохраняем видео
        if output_path is None:
            output_path = TEMP_DIR / f"video_{hash(script)}.mp4"
        
        logger.info(f"💾 Сохранение видео: {output_path}")
        if log_callback:
            log_callback("💾 Сохраняю видео...")
        
        final_clip.write_videofile(
            str(output_path),
            fps=24,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile=str(TEMP_DIR / "temp_audio.m4a"),
            remove_temp=True,
            logger=None  # Отключаем verbose вывод
        )
        
        # 8. Очистка
        audio_clip.close()
        final_clip.close()
        
        logger.info(f"✅ Видео создано: {output_path}")
        logger.info(f"   Размер: {output_path.stat().st_size / 1024 / 1024:.1f} MB")
        if log_callback:
            size_mb = output_path.stat().st_size / 1024 / 1024
            log_callback(f"✅ Видео готово! ({size_mb:.1f} MB)")
        
        # Возвращаем tuple (video_path, audio_path)
        return (output_path, audio_file)
        
    except Exception as e:
        logger.error(f"❌ Ошибка создания видео: {e}")
        raise


# Для совместимости с HeyGen API
def render_video_opensource(script: str, progress_callback=None, log_callback=None, text_position="center", custom_background=None, voice_id=None) -> tuple:
    """
    Обертка для совместимости с renderer.py
    Возвращает tuple (video_url, audio_url) - пути к созданному видео и аудио
    
    Args:
        script: Текст для озвучки
        progress_callback: Функция для обновления статуса (status, elapsed)
        log_callback: Функция для логирования текстовых сообщений
        text_position: Position of text (top, center, bottom)
        custom_background: Custom background image path/URL
        voice_id: ElevenLabs voice ID for TTS
    
    Returns:
        tuple: (video_url, audio_url)
    """
    logger.info(f"📊 Opensource render with: position={text_position}, voice={voice_id}, bg={custom_background is not None}")
    try:
        if progress_callback:
            progress_callback("processing", 0)
        
        # Use custom background or auto-detect category
        if custom_background:
            # Use custom background directly
            category = "custom"
            logger.info(f"🖼️  Using custom background: {custom_background}")
            if log_callback:
                log_callback(f"🖼️  Custom background: {custom_background}")
        else:
            # Auto-detect category from script
            script_lower = script.lower()
            
            if any(word in script_lower for word in ["планета", "planet", "марс", "венера"]):
                category = "planets"
            elif any(word in script_lower for word in ["зодиак", "гороскоп", "астрология", "zodiac"]):
                category = "astrology"
            elif any(word in script_lower for word in ["мистика", "магия", "таро", "mystical"]):
                category = "mystical"
            else:
                category = "space"
            
            logger.info(f"📂 Auto-detected background category: {category}")
            if log_callback:
                log_callback(f"📂 Background category: {category}")
        
        if progress_callback:
            progress_callback("processing", 30)
        
        # Log voice selection
        if voice_id:
            logger.info(f"🎙️  Using selected voice: {voice_id}")
            if log_callback:
                log_callback(f"🎙️  Voice: {voice_id}")
        
        # Создаем видео с custom settings
        if log_callback:
            log_callback("🎬 Создание видео...")
        
        video_path, audio_path = create_opensource_video(
            script=script,
            background_category=category,
            background_index=0,
            voice_lang="ru",
            add_subtitles=True,
            log_callback=log_callback,
            custom_background_path=custom_background if custom_background else None,
            text_position=text_position,
            voice_id=voice_id
        )
        
        if progress_callback:
            progress_callback("completed", 100)
        
        # Возвращаем пути как tuple (video_url, audio_url)
        video_url = f"file://{video_path.absolute()}"
        audio_url = str(audio_path.absolute()) if audio_path else ""
        return (video_url, audio_url)
        
    except Exception as e:
        if progress_callback:
            progress_callback("failed", 0)
        raise


if __name__ == "__main__":
    # Тест
    test_script = """
    Добрый вечер! Сегодня мы поговорим о влиянии планет на нашу жизнь.
    Астрология - древняя наука, которая изучает связь между небесными телами и земными событиями.
    Подписывайтесь на наш канал!
    """
    
    print("🧪 Тестирование open-source генератора видео...")
    
    try:
        video_path = create_opensource_video(
            script=test_script,
            background_category="astrology",
            voice_lang="ru",
            add_subtitles=True
        )
        print(f"✅ Тестовое видео создано: {video_path}")
        
    except Exception as e:
        print(f"❌ Ошибка теста: {e}")

