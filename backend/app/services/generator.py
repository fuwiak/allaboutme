"""Script generation service using Groq API"""
import random
import re
import logging
from groq import Groq
from sqlalchemy.orm import Session
from ..config import settings
from .. import models

logger = logging.getLogger(__name__)

# Initialize Groq client
groq_client = None
if settings.GROQ_API_KEY:
    groq_client = Groq(api_key=settings.GROQ_API_KEY)


def get_setting(db: Session, key: str, default=None):
    """Get setting from database"""
    setting = db.query(models.Setting).filter(models.Setting.key == key).first()
    return setting.value if setting else default


def generate_clean_post(scenario: str, theme: str = "", db: Session = None) -> str:
    """
    Генерирует чистый текст поста из сценария/промпта.
    Возвращает текст без разметки, звездочек, ##, готовый для озвучки.
    
    Args:
        scenario: Контекст/промпт/сценарий для поста
        theme: Тема (опционально)
        db: Database session (optional)
    
    Returns:
        Чистый текст для озвучки
    """
    if not groq_client:
        raise ValueError("GROQ_API_KEY not configured")
    
    try:
        user_prompt = f"""Создай поэтичный, глубокий текст для озвучки эзотерического видео на основе этого сценария:

{scenario}

Пиши красиво, атмосферно, мистически. Используй метафоры, философские вопросы, создавай настроение. 
Текст должен звучать как медитация или мудрое послание.

Пример стиля:
"Ты когда-нибудь слышал, как молчит пространство? В каждом вдохе — тайна, в каждом взгляде — бесконечность. Мы идём сквозь сны, и каждый миг — это выбор между светом и тенью. Помни: мир снаружи лишь эхо того, что рождается внутри тебя."

Напиши текст для озвучки:"""
        
        completion = groq_client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "Ты — мистический поэт и философ. Создаёшь глубокие, атмосферные тексты для эзотерических видео. Пиши красиво, образно, вдохновляюще."},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.95,
            max_tokens=1000
        )
        
        raw_text = completion.choices[0].message.content.strip()
        logger.info(f"📝 Получен текст от GPT ({len(raw_text)} символов)")
        logger.info(f"📄 Текст: {raw_text[:200]}...")
        
        # Минимальная очистка - только явная разметка
        clean_text = raw_text
        
        # Убираем только очевидную разметку
        clean_text = re.sub(r'\*\*(.+?)\*\*', r'\1', clean_text)  # **bold**
        clean_text = re.sub(r'\*(.+?)\*', r'\1', clean_text)  # *italic*
        clean_text = re.sub(r'#+\s*', '', clean_text)  # ### headers
        clean_text = re.sub(r'\[.+?\]:\s*', '', clean_text)  # [технические указания]:
        clean_text = re.sub(r'\n{3,}', '\n\n', clean_text)  # лишние переносы
        clean_text = clean_text.strip()
        
        logger.info(f"✅ Чистый текст готов ({len(clean_text)} символов)")
        
        # Если текст слишком короткий - возвращаем оригинал
        if len(clean_text) < 20:
            logger.warning(f"⚠️ Текст слишком короткий после очистки, возвращаем оригинал")
            return raw_text
        
        return clean_text
        
    except Exception as e:
        logger.error(f"Ошибка генерации чистого текста: {e}")
        # Возвращаем исходный сценарий с базовой очисткой
        clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', scenario)
        clean = re.sub(r'\*([^*]+)\*', r'\1', clean)
        clean = re.sub(r'##\s*', '', clean)
        clean = re.sub(r'\[([^\]]+)\]', '', clean)
        return clean.strip()


def generate_scripts(db: Session, count: int = 1) -> list[dict]:
    """
    Генерирует сценарии для видео
    
    Args:
        db: Database session
        count: Количество сценариев для генерации
    
    Returns:
        Список словарей {script, hook, caption, theme}
    """
    if not groq_client:
        raise ValueError("GROQ_API_KEY not configured")
    
    try:
        # Получаем настройки из БД
        themes_str = get_setting(db, "themes", "daily horoscope,funny Mercury retrograde fact")
        themes = [t.strip() for t in themes_str.split(",")]
        
        system_prompt = get_setting(
            db,
            "system_prompt",
            "You are a witty astrologer & numerologist. Write short, hooky 15-30 s video scripts about astrology, numerology, Human Design or Matrix of Destiny, always ending with a call to action. write in russian"
        )
        
        caption_template = get_setting(
            db,
            "caption_template",
            "{hook}\n\n#astrology #numerology #humandesign #shorts"
        )
        
        scripts = []
        themes_today = random.sample(themes, k=min(len(themes), count))
        
        for i in range(count):
            theme = random.choice(themes_today) if themes_today else "astrology"
            logger.info(f"Генерация сценария {i+1}/{count} на тему: {theme}")
            
            user_prompt = f"Topic: {theme}. Give me a punchy 15-30 second video script."
            
            try:
                completion = groq_client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.8,
                    max_tokens=500
                )
                
                script = completion.choices[0].message.content.strip()
                hook = script.split("\n")[0][:80]  # первая строка = хук
                caption = caption_template.format(hook=hook)
                
                script_data = {
                    "theme": theme,
                    "script": script,
                    "hook": hook,
                    "caption": caption
                }
                
                scripts.append(script_data)
                logger.info(f"Сценарий {i+1} успешно создан: {hook}")
                
            except Exception as e:
                logger.error(f"Ошибка при генерации сценария {i+1}: {e}")
                continue
        
        logger.info(f"Всего создано сценариев: {len(scripts)}")
        return scripts
        
    except Exception as e:
        logger.error(f"Критическая ошибка в generate_scripts: {e}")
        raise

