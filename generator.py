import random, os, yaml, logging
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

cfg = yaml.safe_load(open("config.yaml"))
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("astro.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def generate_clean_post(scenario: str, theme: str = "") -> str:
    """
    Генерирует чистый текст поста из сценария/промпта.
    Возвращает текст без разметки, звездочек, ##, готовый для озвучки.
    
    Args:
        scenario: Контекст/промпт/сценарий для поста
        theme: Тема (опционально)
    
    Returns:
        Чистый текст для озвучки
    """
    try:
        user_prompt = f"""Создай поэтичный, глубокий текст для озвучки эзотерического видео на основе этого сценария:

{scenario}

Пиши красиво, атмосферно, мистически. Используй метафоры, философские вопросы, создавай настроение. 
Текст должен звучать как медитация или мудрое послание.

Пример стиля:
"Ты когда-нибудь слышал, как молчит пространство? В каждом вдохе — тайна, в каждом взгляде — бесконечность. Мы идём сквозь сны, и каждый миг — это выбор между светом и тенью. Помни: мир снаружи лишь эхо того, что рождается внутри тебя."

Напиши текст для озвучки:"""
        
        completion = client.chat.completions.create(
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
        import re
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
        import re
        clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', scenario)
        clean = re.sub(r'\*([^*]+)\*', r'\1', clean)
        clean = re.sub(r'##\s*', '', clean)
        clean = re.sub(r'\[([^\]]+)\]', '', clean)
        return clean.strip()

def generate_scripts(send_to_approval=True) -> list[dict]:
    """
    Возвращает список словарей {script, hook, caption, theme}.
    
    Args:
        send_to_approval: Если True - отправляет сценарии на одобрение в Telegram
                         Если False - просто возвращает список
    """
    try:
        themes_today = random.sample(cfg["themes"], k=len(cfg["themes"]))
        scripts = []
        
        for i in range(cfg["daily_videos"]):
            theme = random.choice(themes_today)
            logger.info(f"Генерация сценария {i+1}/{cfg['daily_videos']} на тему: {theme}")
            
            user_prompt = f"Topic: {theme}. Give me a punchy 15-30 second video script."
            
            try:
                completion = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role": "system", "content": cfg["system_prompt"]},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.8,
                    max_tokens=500
                )
                
                script = completion.choices[0].message.content.strip()
                hook = script.split("\n")[0][:80]  # первая строка = хук
                caption = cfg.get("caption_template", "{hook}").format(hook=hook)
                
                script_data = {
                    "theme": theme,
                    "script": script,
                    "hook": hook,
                    "caption": caption
                }
                
                scripts.append(script_data)
                logger.info(f"Сценарий {i+1} успешно создан: {hook}")
                
                # Отправляем на одобрение в Telegram
                if send_to_approval:
                    try:
                        import asyncio
                        from bot import send_script_for_approval
                        asyncio.run(send_script_for_approval(script_data))
                    except Exception as e:
                        logger.error(f"Ошибка отправки сценария на одобрение: {e}")
                
            except Exception as e:
                logger.error(f"Ошибка при генерации сценария {i+1}: {e}")
                # Отправляем уведомление в Telegram
                try:
                    import asyncio
                    from bot import send_error_notification
                    asyncio.run(send_error_notification(f"❌ Ошибка генерации сценария {i+1}: {str(e)}"))
                except:
                    pass
                continue
        
        logger.info(f"Всего создано сценариев: {len(scripts)}")
        
        if send_to_approval and scripts:
            logger.info(f"✅ {len(scripts)} сценариев отправлено на одобрение в Telegram")
        
        return scripts
        
    except Exception as e:
        logger.error(f"Критическая ошибка в generate_scripts: {e}")
        try:
            import asyncio
            from bot import send_error_notification
            asyncio.run(send_error_notification(f"❌ Критическая ошибка генерации: {str(e)}"))
        except:
            pass
        raise