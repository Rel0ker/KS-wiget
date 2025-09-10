#!/usr/bin/env python
"""
Скрипт для создания тестовых данных в базе данных
"""
import os
import sys
import django
from datetime import datetime, time

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ks_widget.settings_production')
django.setup()

from groups.models import LanguageLevel, DayOfWeek, TimeSlot, Group, GroupSchedule

def create_language_levels():
    """Создание уровней языков"""
    levels_data = [
        {'name': 'Начальный', 'order': 1, 'description': 'Для начинающих изучать корейский язык'},
        {'name': 'Элементарный', 'order': 2, 'description': 'Базовые знания корейского языка'},
        {'name': 'Средний', 'order': 3, 'description': 'Средний уровень владения корейским языком'},
        {'name': 'Продвинутый', 'order': 4, 'description': 'Продвинутый уровень корейского языка'},
        {'name': 'Высший', 'order': 5, 'description': 'Высший уровень владения корейским языком'},
    ]
    
    for level_data in levels_data:
        level, created = LanguageLevel.objects.get_or_create(
            name=level_data['name'],
            defaults=level_data
        )
        if created:
            print(f"Создан уровень: {level.name}")
        else:
            print(f"Уровень уже существует: {level.name}")

def create_days_of_week():
    """Создание дней недели"""
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
            print(f"Создан день: {day.name}")
        else:
            print(f"День уже существует: {day.name}")

def create_time_slots():
    """Создание временных слотов"""
    time_slots_data = [
        {'start_time': time(9, 0), 'end_time': time(10, 30)},
        {'start_time': time(10, 30), 'end_time': time(12, 0)},
        {'start_time': time(12, 0), 'end_time': time(13, 30)},
        {'start_time': time(13, 30), 'end_time': time(15, 0)},
        {'start_time': time(15, 0), 'end_time': time(16, 30)},
        {'start_time': time(16, 30), 'end_time': time(18, 0)},
        {'start_time': time(18, 0), 'end_time': time(19, 30)},
        {'start_time': time(19, 30), 'end_time': time(21, 0)},
    ]
    
    for slot_data in time_slots_data:
        slot, created = TimeSlot.objects.get_or_create(
            start_time=slot_data['start_time'],
            end_time=slot_data['end_time'],
            defaults=slot_data
        )
        if created:
            print(f"Создан временной слот: {slot.start_time} - {slot.end_time}")
        else:
            print(f"Временной слот уже существует: {slot.start_time} - {slot.end_time}")

def create_groups():
    """Создание групп"""
    import random
    
    # Получаем уровни и временные слоты
    levels = list(LanguageLevel.objects.all())
    days = list(DayOfWeek.objects.all())
    time_slots = list(TimeSlot.objects.all())
    
    if not levels or not days or not time_slots:
        print("Ошибка: Не все базовые данные созданы!")
        return
    
    groups_data = [
        {
            'name': 'Корейский для начинающих (утро)',
            'description': 'Изучение основ корейского языка для тех, кто только начинает свой путь. Группа подходит для полных новичков.',
            'level': levels[0],  # Начальный
            'total_capacity': 12,
            'is_active': True
        },
        {
            'name': 'Корейский для начинающих (вечер)',
            'description': 'Вечерняя группа для изучения основ корейского языка. Удобное время для работающих студентов.',
            'level': levels[0],  # Начальный
            'total_capacity': 10,
            'is_active': True
        },
        {
            'name': 'Элементарный корейский (дневная группа)',
            'description': 'Продолжение изучения корейского языка для тех, кто уже знает основы. Изучаем грамматику и расширяем словарный запас.',
            'level': levels[1],  # Элементарный
            'total_capacity': 8,
            'is_active': True
        },
        {
            'name': 'Элементарный корейский (выходные)',
            'description': 'Группа выходного дня для продолжающих изучение корейского языка. Интенсивные занятия по субботам.',
            'level': levels[1],  # Элементарный
            'total_capacity': 6,
            'is_active': True
        },
        {
            'name': 'Средний уровень (утренняя группа)',
            'description': 'Для студентов со средним уровнем корейского языка. Изучаем сложную грамматику и практикуем разговорную речь.',
            'level': levels[2],  # Средний
            'total_capacity': 8,
            'is_active': True
        },
        {
            'name': 'Средний уровень (вечерняя группа)',
            'description': 'Вечерняя группа для студентов среднего уровня. Удобное время для работающих людей.',
            'level': levels[2],  # Средний
            'total_capacity': 10,
            'is_active': True
        },
        {
            'name': 'Продвинутый корейский (интенсив)',
            'description': 'Интенсивный курс для продвинутых студентов. Глубокое изучение языка и культуры Кореи.',
            'level': levels[3],  # Продвинутый
            'total_capacity': 6,
            'is_active': True
        },
        {
            'name': 'Продвинутый корейский (разговорная практика)',
            'description': 'Группа для практики разговорной речи на продвинутом уровне. Обсуждение актуальных тем и культурных аспектов.',
            'level': levels[3],  # Продвинутый
            'total_capacity': 8,
            'is_active': True
        },
        {
            'name': 'Высший уровень (академический)',
            'description': 'Академический курс корейского языка для студентов высшего уровня. Подготовка к экзаменам и профессиональному использованию.',
            'level': levels[4],  # Высший
            'total_capacity': 5,
            'is_active': True
        },
        {
            'name': 'Корейский для бизнеса',
            'description': 'Специализированный курс корейского языка для делового общения. Изучаем бизнес-терминологию и этикет.',
            'level': levels[3],  # Продвинутый
            'total_capacity': 8,
            'is_active': True
        },
        {
            'name': 'Корейская культура и язык',
            'description': 'Комплексный курс изучения корейского языка через призму культуры. Изучаем традиции, обычаи и современную культуру Кореи.',
            'level': levels[2],  # Средний
            'total_capacity': 10,
            'is_active': True
        },
        {
            'name': 'Подготовка к TOPIK',
            'description': 'Специализированный курс подготовки к экзамену TOPIK (Test of Proficiency in Korean). Интенсивная подготовка к сдаче экзамена.',
            'level': levels[3],  # Продвинутый
            'total_capacity': 6,
            'is_active': True
        },
        {
            'name': 'Корейский для путешествий',
            'description': 'Практический курс корейского языка для путешественников. Изучаем фразы и выражения, необходимые в поездке по Корее.',
            'level': levels[1],  # Элементарный
            'total_capacity': 12,
            'is_active': True
        },
        {
            'name': 'Корейский через K-Pop',
            'description': 'Инновационный подход к изучению корейского языка через популярную музыку. Изучаем язык через песни и клипы.',
            'level': levels[1],  # Элементарный
            'total_capacity': 15,
            'is_active': True
        },
        {
            'name': 'Корейский для детей',
            'description': 'Специальная программа изучения корейского языка для детей. Игровая форма обучения с использованием мультфильмов и песен.',
            'level': levels[0],  # Начальный
            'total_capacity': 8,
            'is_active': True
        }
    ]
    
    for group_data in groups_data:
        group, created = Group.objects.get_or_create(
            name=group_data['name'],
            defaults=group_data
        )
        if created:
            print(f"Создана группа: {group.name}")
            
            # Создаем расписание для группы (случайные дни и время)
            num_schedule_items = random.randint(1, 3)  # 1-3 занятия в неделю
            selected_days = random.sample(days, min(num_schedule_items, len(days)))
            selected_times = random.sample(time_slots, min(num_schedule_items, len(time_slots)))
            
            for i, day in enumerate(selected_days):
                time_slot = selected_times[i] if i < len(selected_times) else selected_times[0]
                
                schedule, created = GroupSchedule.objects.get_or_create(
                    group=group,
                    day_of_week=day,
                    time_slot=time_slot
                )
                if created:
                    print(f"  - Расписание: {day.name} {time_slot.start_time}-{time_slot.end_time}")
        else:
            print(f"Группа уже существует: {group.name}")

def main():
    print("Создание тестовых данных...")
    print("=" * 50)
    
    print("\n1. Создание уровней языков...")
    create_language_levels()
    
    print("\n2. Создание дней недели...")
    create_days_of_week()
    
    print("\n3. Создание временных слотов...")
    create_time_slots()
    
    print("\n4. Создание групп...")
    create_groups()
    
    print("\n" + "=" * 50)
    print("Тестовые данные созданы успешно!")
    
    # Выводим статистику
    print(f"\nСтатистика:")
    print(f"- Уровней языков: {LanguageLevel.objects.count()}")
    print(f"- Дней недели: {DayOfWeek.objects.count()}")
    print(f"- Временных слотов: {TimeSlot.objects.count()}")
    print(f"- Групп: {Group.objects.count()}")
    print(f"- Расписаний: {GroupSchedule.objects.count()}")

if __name__ == '__main__':
    main()
