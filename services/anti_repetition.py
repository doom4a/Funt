"""
Anti-Repetition Engine для Funt 3.0

Решает проблему повторяющихся фраз типа:
"Ахаха, X? Это как моя верность Лильке — вроде Y..."
"""

import re
from typing import List, Set
from datetime import datetime, timedelta


class AntiRepetitionEngine:
    """Умная система против повторений"""
    
    def __init__(self):
        self.recent_responses: List[str] = []
        self.phrase_patterns: Set[str] = set()
        self.banned_templates: List[str] = []
        self.max_history = 50
        
    def add_response(self, response: str):
        """Сохранить ответ в историю"""
        self.recent_responses.append(response)
        if len(self.recent_responses) > self.max_history:
            self.recent_responses.pop(0)
        
        # Извлечь паттерн
        pattern = self._extract_pattern(response)
        if pattern:
            self.phrase_patterns.add(pattern)
    
    def is_too_similar(self, new_response: str) -> bool:
        """Проверка на повторение"""
        # Проверка 1: Точное совпадение
        if new_response in self.recent_responses:
            return True
        
        # Проверка 2: Шаблон повторяется
        new_pattern = self._extract_pattern(new_response)
        if new_pattern and new_pattern in self.phrase_patterns:
            return True
        
        # Проверка 3: Структурный скелет повторяется
        new_skeleton = self._extract_structural_skeleton(new_response)
        for old_response in self.recent_responses[-10:]:  # Проверяем последние 10
            old_skeleton = self._extract_structural_skeleton(old_response)
            if new_skeleton == old_skeleton and len(new_skeleton) > 20:  # Игнорируем короткие
                return True
        
        # Проверка 4: Совпадение начала фразы (первые 3 слова)
        new_prefix = " ".join(self._normalize(new_response).split()[:3])
        if new_prefix:
            for old_response in self.recent_responses[-15:]:
                old_prefix = " ".join(self._normalize(old_response).split()[:3])
                if old_prefix and old_prefix == new_prefix:
                    return True
        
        # Проверка 5: Jaccard similarity > 0.5 (чуть строже по повторам)
        for old_response in self.recent_responses[-20:]:
            similarity = self._jaccard_similarity(new_response, old_response)
            if similarity > 0.5:
                return True
        
        # Проверка 6: Запрещенные шаблоны
        for banned in self.banned_templates:
            if banned.lower() in new_response.lower():
                return True
        
        return False
    
    def _extract_pattern(self, text: str) -> str:
        """Извлечь паттерн из текста"""
        # Ищем повторяющиеся конструкции
        patterns = [
            r'Ахаха, .+? Это как моя верность Лильке',
            r'Это как твоя логика — вроде',
            r'Unian уже завтра напишет',
            r'А я как всегда — налоги плачу',
        ]
        
        for pattern in patterns:
            if re.search(pattern, text):
                return pattern
        
        return ""
    
    def _extract_structural_skeleton(self, text: str) -> str:
        """Извлечь структурный скелет ответа (без конкретных слов)"""
        # Убираем имена собственные и заменяем на маркеры
        skeleton = text
        
        # Заменяем имена на {NAME}
        skeleton = re.sub(r'\b(Ваван|Дум|Скот|Владимир|Дмитрий|Алексей)\b', '{NAME}', skeleton)
        
        # Заменяем города на {PLACE}
        skeleton = re.sub(r'\b(Домодедово|Калининград|Минск|Москва)\b', '{PLACE}', skeleton)
        
        # Заменяем хобби/предметы на {HOBBY}
        skeleton = re.sub(r'\b(бадминтон|волан|ракетк[аи]|рыбалк[аеи]|судак[аи]?)\b', '{HOBBY}', skeleton)
        
        # Заменяем оскорбления на {INSULT}
        skeleton = re.sub(r'\b(замкадыш|ебан[ая]|гавно|хуй|пизд[аеу])\b', '{INSULT}', skeleton, flags=re.IGNORECASE)
        
        # Убираем лишние пробелы
        skeleton = re.sub(r'\s+', ' ', skeleton).strip()
        
        return skeleton
    
    def _normalize(self, text: str) -> str:
        """Очистка текста для сравнения"""
        # Удаляем пунктуацию и приводим к нижнему регистру
        text = re.sub(r'[^\w\s]', '', text.lower())
        return text.strip()

    def _jaccard_similarity(self, text1: str, text2: str) -> float:
        """Вычислить схожесть текстов"""
        # Нормализуем тексты
        t1 = self._normalize(text1)
        t2 = self._normalize(text2)
        
        words1 = set(t1.split())
        words2 = set(t2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0
    
    def update_banned_templates(self):
        """Обновить список запрещенных шаблонов"""
        # На основе частоты использования
        pattern_freq = {}
        for response in self.recent_responses[-30:]:
            pattern = self._extract_pattern(response)
            if pattern:
                pattern_freq[pattern] = pattern_freq.get(pattern, 0) + 1
        
        # Если паттерн встречается > 3 раз за последние 30 сообщений — ban
        self.banned_templates = [
            pattern for pattern, freq in pattern_freq.items()
            if freq > 3
        ]
