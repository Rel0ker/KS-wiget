#!/usr/bin/env python
"""
Скрипт для создания начальных данных в системе KS Widget
Запускать после создания суперпользователя
"""

import os
import sys
import django
from datetime import date, timedelta

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ks_widget.settings')
django.setup()

from groups.models import LanguageLevel, Group, DayOfWeek, TimeSlot
from django.contrib.auth.models import User

def create_initial_data():
    """Создание начальных данных"""
    
    print("Создание начальных данных для KS Widget...")
    
    # Создание дней недели
    days_data = [
        {'name': 'monday', 'order': 1},
        {'name': 'tuesday', 'order': 2},
        {'name': 'wednesday', 'order': 3},
        {'name': 'thursday', 'order': 4},
        {'name': 'friday', 'order': 5},
        {'name': 'saturday', 'order': 6},
        {'name': 'sunday', 'order': 7},
    ]
    
    for day_data in days_data:
        day, created = DayOfWeek.objects.get_or_create(
            name=day_data['name'],
            defaults=day_data
        )
        if created:
            print(f"✓ Создан день недели: {day}")
        else:
            print(f"○ День недели уже существует: {day}")
    
    # Создание временных слотов
    time_slots_data = [
        {'start_time': '09:00', 'end_time': '10:30'},
        {'start_time': '10:00', 'end_time': '11:30'},
        {'start_time': '11:00', 'end_time': '12:30'},
        {'start_time': '12:00', 'end_time': '13:30'},
        {'start_time': '13:00', 'end_time': '14:30'},
        {'start_time': '14:00', 'end_time': '15:30'},
        {'start_time': '15:00', 'end_time': '16:30'},
        {'start_time': '16:00', 'end_time': '17:30'},
        {'start_time': '17:00', 'end_time': '18:30'},
        {'start_time': '18:00', 'end_time': '19:30'},
        {'start_time': '19:00', 'end_time': '20:30'},
        {'start_time': '20:00', 'end_time': '21:30'},
        {'start_time': '21:00', 'end_time': '22:30'},
    ]
    
    for slot_data in time_slots_data:
        slot, created = TimeSlot.objects.get_or_create(
            start_time=slot_data['start_time'],
            end_time=slot_data['end_time'],
            defaults=slot_data
        )
        if created:
            print(f"✓ Создан временной слот: {slot}")
        else:
            print(f"○ Временной слот уже существует: {slot}")
    
    # Создание уровней языка
    levels_data = [
        {
            'name': 'Начинающий (Beginner)',
            'description': 'Для тех, кто только начинает изучать корейский язык',
            'order': 1
        },
        {
            'name': 'Средний (Intermediate)',
            'description': 'Для тех, кто уже знает основы корейского языка',
            'order': 2
        },
        {
            'name': 'Продвинутый (Advanced)',
            'description': 'Для тех, кто свободно владеет корейским языком',
            'order': 3
        }
    ]
    
    levels = []
    for level_data in levels_data:
        level, created = LanguageLevel.objects.get_or_create(
            name=level_data['name'],
            defaults=level_data
        )
        levels.append(level)
        if created:
            print(f"✓ Создан уровень: {level.name}")
        else:
            print(f"○ Уровень уже существует: {level.name}")
    
    # Создание групп
    groups_data = [
        {
            'name': 'Корейский для начинающих - Группа А',
            'level': levels[0],
            'total_capacity': 15,
            'current_participants': 8,
            'color': '#3B82F6',
            'description': 'Курс для тех, кто только начинает изучать корейский язык. Изучаем алфавит, базовые фразы и грамматику.',
            'start_date': date.today() + timedelta(days=7),
            'schedule': 'Понедельник, Среда, Пятница 18:00-19:30',
            'is_active': True
        },
        {
            'name': 'Корейский для начинающих - Группа Б',
            'level': levels[0],
            'total_capacity': 12,
            'current_participants': 5,
            'color': '#10B981',
            'description': 'Вторая группа для начинающих. Изучаем основы корейского языка в удобное время.',
            'start_date': date.today() + timedelta(days=14),
            'schedule': 'Вторник, Четверг 19:00-20:30',
            'is_active': True
        },
        {
            'name': 'Корейский средний уровень',
            'level': levels[1],
            'total_capacity': 10,
            'current_participants': 7,
            'color': '#F59E0B',
            'description': 'Курс для продолжающих изучение. Углубляем знания грамматики, расширяем словарный запас.',
            'start_date': date.today() + timedelta(days=3),
            'schedule': 'Понедельник, Четверг 20:00-21:30',
            'is_active': True
        },
        {
            'name': 'Корейский продвинутый уровень',
            'level': levels[2],
            'total_capacity': 8,
            'current_participants': 6,
            'color': '#EF4444',
            'description': 'Курс для продвинутых студентов. Изучаем сложную грамматику, читаем литературу, смотрим фильмы.',
            'start_date': date.today() + timedelta(days=1),
            'schedule': 'Среда, Суббота 19:00-21:00',
            'is_active': True
        },
        {
            'name': 'Разговорный корейский',
            'level': levels[1],
            'total_capacity': 12,
            'current_participants': 4,
            'color': '#8B5CF6',
            'description': 'Специальный курс для развития разговорных навыков. Много практики общения.',
            'start_date': date.today() + timedelta(days=21),
            'schedule': 'Пятница 18:00-20:00, Суббота 10:00-12:00',
            'is_active': True
        }
    ]
    
    for group_data in groups_data:
        group, created = Group.objects.get_or_create(
            name=group_data['name'],
            defaults=group_data
        )
        if created:
            print(f"✓ Создана группа: {group.name}")
        else:
            print(f"○ Группа уже существует: {group.name}")
    
    print("\n✅ Начальные данные созданы успешно!")
    print("\n📊 Статистика:")
    print(f"   - Дней недели: {DayOfWeek.objects.count()}")
    print(f"   - Временных слотов: {TimeSlot.objects.count()}")
    print(f"   - Уровней языка: {LanguageLevel.objects.count()}")
    print(f"   - Групп: {Group.objects.count()}")
    print(f"   - Активных групп: {Group.objects.filter(is_active=True).count()}")
    
    print("\n🔗 Ссылки для доступа:")
    print("   - Админ-панель Django: http://localhost:8000/admin/")
    print("   - API документация: http://localhost:8000/api/docs/")
    print("   - Frontend админ-панель: http://localhost:3000")
    print("   - Виджет: http://localhost:3000/widget/")

if __name__ == '__main__':
    try:
        create_initial_data()
    except Exception as e:
        print(f"❌ Ошибка при создании данных: {e}")
        sys.exit(1)
