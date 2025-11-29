# Инструкция по Интеграции Фунта 3.0

## Быстрая Интеграция (5 минут)

### Шаг 1: Добавить импорты

Откройте `Funt_2.0.py` и **после строки 20** (после `from typing import Optional, List, Dict, Any`) добавьте:

```python
# ─── Импорт новых компонентов Фунт 3.0 ─────────────────
try:
    from services.anti_repetition import AntiRepetitionEngine
    from services.provocation_system import ProvocationSystem
except ImportError:
    # Fallback если модули не найдены
    AntiRepetitionEngine = None
    ProvocationSystem = None
    logging.warning("Фунт 3.0 компоненты не найдены, работаем в базовом режиме")
```

---

### Шаг 2: Инициализировать компоненты

**После строки 68** (после определения `used_jokes`) добавьте:

```python
# ─── Новые компоненты Фунт 3.0 ───────────────────────────
# Anti-Repetition Engine
anti_repetition_engine = AntiRepetitionEngine() if AntiRepetitionEngine else None

# Provocation System  
provocation_system = ProvocationSystem() if ProvocationSystem else None

# Загрузка расширенных событий
life_events_extended = []
try:
    with open('data/life_events_extended.json', 'r', encoding='utf-8') as f:
        events_data = json.load(f)
        for category in ['family_events', 'work_events', 'daily_life', 'news_reactions']:
            life_events_extended.extend(events_data.get(category, []))
    logging.info(f"✅ Загружено {len(life_events_extended)} расширенных событий")
except FileNotFoundError:
    logging.warning("life_events_extended.json не найден, используем базовые события")

# Загрузка расширенных мемов
memes_extended = {}
try:
    with open('data/memes_extended.json', 'r', encoding='utf-8') as f:
        memes_extended = json.load(f)
    logging.info("✅ Загружены расширенные мемы")
except FileNotFoundError:
    logging.warning("memes_extended.json не найден")
```

---

### Шаг 3: Модифицировать generate_life_event

Найдите функцию `async def generate_life_event(mood_sys: MoodSystem)` (примерно строка 442).

**В начале функции** (сразу после docstring) добавьте:

```python
    # Приоритет 1: Использовать расширенную базу событий
    if life_events_extended:
        # Фильтруем события которых недавно не было
        recent_ids = [ev.event_id for ev in mood_sys.event_history[-10:]]
        available_events = [
            ev for ev in life_events_extended
            if ev.get('id') not in recent_ids
        ]
        
        if available_events:
            # Выбираем случайное событие
            event_data = random.choice(available_events)
            
            event = Event(
                event_id=event_data.get('id', f'event_{int(datetime.now().timestamp())}'),
                event_text=event_data.get('text', 'Неопределенное событие'),
                details=event_data.get('details', ''),
                mood=event_data.get('mood', 'CONTENT'),
                intensity=float(event_data.get('intensity', 0.7)),
                duration_hours=int(event_data.get('duration_hours', 6)),
                trigger_phrases=event_data.get('trigger_phrases', [])
            )
            
            logging.info(f"🎉 Событие из базы: {event.mood} ({event.intensity:.0%})")
            return event
    
    # Приоритет 2: Генерация через AI (если база исчерпана)
```

---

### Шаг 4: Добавить Anti-Repetition в generate_funt_response

Найдите функцию `generate_funt_response` (примерно строка 740).

**После блока** где content получен из API (примерно строка 810), **перед** `if any(p in content for p in fraz_list):` добавьте:

```python
    # 💚 Anti-Repetition Check (Funt 3.0)
    if anti_repetition_engine and not is_news:
        # Проверяем на повторение
        if anti_repetition_engine.is_too_similar(content):
            logging.warning("⚠️ Ответ слишком похож на предыдущие! Регенерируем...")
            # Повышаем temperature для большей креативности
            payload["temperature"] = min(1.2, TEMPERATURE_RESPONSE + 0.3)
            
            try:
                response = await client.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"].strip()
                logging.info("✅ Регенерация успешна")
            except Exception as e:
                logging.warning(f"Регенерация не удалась: {e}")
        
        # Сохраняем ответ в историю
        anti_repetition_engine.add_response(content)
        # Обновляем список запрещенных шаблонов
        anti_repetition_engine.update_banned_templates()
```

---

### Шаг 5: Добавить провокации в initiate_conversation

Найдите функцию `initiate_conversation` (примерно строка 880).

**В начале функции** (после определения `app`) добавьте:

```python
    # 🎯 Используем провокации из Funt 3.0
    current_hour = datetime.now().hour
    
    if provocation_system and provocation_system.should_provoke(current_hour):
        provocation = provocation_system.generate_provocation()
        if provocation:
            await app.bot.send_message(chat_id=CHAT_ID, text=provocation)
            bot_metrics['bot_messages'] += 1
            bot_metrics['proactive_messages'] += 1
            logging.info(f"💥 Провокация отправлена: {provocation[:50]}...")
            return
```

---

## Готово! 🎉

**Запустить бота:**
```bash
cd /Volumes/Внешний/Python/funt_bot_d
python3 Funt_2.0.py
```

**Проверить работу:**
1. Бот не должен повторять "Ахаха, X? Это как моя верность Лильке..."
2. В логах появятся: "✅ Загружено X расширенных событий"
3. Провокации будут отправляться в 9-18

---

## Альтернатива: Автоматический патч

Если хотите автоматически - запустите:

```bash
cd /Volumes/Внешний/Python/funt_bot_d
python3 scripts/apply_funt_3_patch.py
```

(Скрипт будет создан отдельно если нужно)
