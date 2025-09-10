#!/usr/bin/env python
"""
Скрипт для создания групп с новыми уровнями
"""
import os
import sys
import django
from datetime import datetime, time
import random

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ks_widget.settings_production')
django.setup()

from groups.models import LanguageLevel, DayOfWeek, TimeSlot, Group, GroupSchedule

def create_groups():
    """Создание групп с новыми уровнями"""
    
    # Получаем уровни, дни и временные слоты
    levels = list(LanguageLevel.objects.all())
    days = list(DayOfWeek.objects.all())
    time_slots = list(TimeSlot.objects.all())
    
    if not levels or not days or not time_slots:
        print("Ошибка: Не все базовые данные созданы!")
        return
    
    # Маппинг уровней
    level_map = {level.name: level for level in levels}
    
    groups_data = [
        # Начинающие (5 групп)
        {
            'name': 'Корейский для начинающих (утро)',
            'description': 'Изучение основ корейского языка для тех, кто только начинает свой путь. Группа подходит для полных новичков.',
            'level': level_map['Начинающие'],
            'total_capacity': 12,
            'is_active': True
        },
        {
            'name': 'Корейский для начинающих (вечер)',
            'description': 'Вечерняя группа для изучения основ корейского языка. Удобное время для работающих студентов.',
            'level': level_map['Начинающие'],
            'total_capacity': 10,
            'is_active': True
        },
        {
            'name': 'Корейский для путешествий',
            'description': 'Практический курс корейского языка для путешественников. Изучаем фразы и выражения, необходимые в поездке по Корее.',
            'level': level_map['Начинающие'],
            'total_capacity': 12,
            'is_active': True
        },
        {
            'name': 'Корейский через K-Pop',
            'description': 'Инновационный подход к изучению корейского языка через популярную музыку. Изучаем язык через песни и клипы.',
            'level': level_map['Начинающие'],
            'total_capacity': 15,
            'is_active': True
        },
        {
            'name': 'Корейский для детей',
            'description': 'Специальная программа изучения корейского языка для детей. Игровая форма обучения с использованием мультфильмов и песен.',
            'level': level_map['Начинающие'],
            'total_capacity': 8,
            'is_active': True
        },
        
        # Средний уровень (5 групп)
        {
            'name': 'Средний уровень (утренняя группа)',
            'description': 'Для студентов со средним уровнем корейского языка. Изучаем сложную грамматику и практикуем разговорную речь.',
            'level': level_map['Средний уровень'],
            'total_capacity': 8,
            'is_active': True
        },
        {
            'name': 'Средний уровень (вечерняя группа)',
            'description': 'Вечерняя группа для студентов среднего уровня. Удобное время для работающих людей.',
            'level': level_map['Средний уровень'],
            'total_capacity': 10,
            'is_active': True
        },
        {
            'name': 'Корейская культура и язык',
            'description': 'Комплексный курс изучения корейского языка через призму культуры. Изучаем традиции, обычаи и современную культуру Кореи.',
            'level': level_map['Средний уровень'],
            'total_capacity': 10,
            'is_active': True
        },
        {
            'name': 'Элементарный корейский (дневная группа)',
            'description': 'Продолжение изучения корейского языка для тех, кто уже знает основы. Изучаем грамматику и расширяем словарный запас.',
            'level': level_map['Средний уровень'],
            'total_capacity': 8,
            'is_active': True
        },
        {
            'name': 'Элементарный корейский (выходные)',
            'description': 'Группа выходного дня для продолжающих изучение корейского языка. Интенсивные занятия по субботам.',
            'level': level_map['Средний уровень'],
            'total_capacity': 6,
            'is_active': True
        },
        
        # Продвинутые (5 групп)
        {
            'name': 'Продвинутый корейский (интенсив)',
            'description': 'Интенсивный курс для продвинутых студентов. Глубокое изучение языка и культуры Кореи.',
            'level': level_map['Продвинутые'],
            'total_capacity': 6,
            'is_active': True
        },
        {
            'name': 'Продвинутый корейский (разговорная практика)',
            'description': 'Группа для практики разговорной речи на продвинутом уровне. Обсуждение актуальных тем и культурных аспектов.',
            'level': level_map['Продвинутые'],
            'total_capacity': 8,
            'is_active': True
        },
        {
            'name': 'Корейский для бизнеса',
            'description': 'Специализированный курс корейского языка для делового общения. Изучаем бизнес-терминологию и этикет.',
            'level': level_map['Продвинутые'],
            'total_capacity': 8,
            'is_active': True
        },
        {
            'name': 'Подготовка к TOPIK',
            'description': 'Специализированный курс подготовки к экзамену TOPIK (Test of Proficiency in Korean). Интенсивная подготовка к сдаче экзамена.',
            'level': level_map['Продвинутые'],
            'total_capacity': 6,
            'is_active': True
        },
        {
            'name': 'Высший уровень (академический)',
            'description': 'Академический курс корейского языка для студентов высшего уровня. Подготовка к экзаменам и профессиональному использованию.',
            'level': level_map['Продвинутые'],
            'total_capacity': 5,
            'is_active': True
        }
    ]
    
    for group_data in groups_data:
        group, created = Group.objects.get_or_create(
            name=group_data['name'],
            defaults=group_data
        )
        if created:
            print(f"Создана группа: {group.name} ({group.level.name})")
            
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
    print("Создание групп с новыми уровнями...")
    print("=" * 50)
    
    print("\nСоздание групп...")
    create_groups()
    
    print("\n" + "=" * 50)
    print("Группы созданы успешно!")
    
    # Выводим статистику
    print(f"\nСтатистика:")
    print(f"- Уровней языков: {LanguageLevel.objects.count()}")
    print(f"- Групп: {Group.objects.count()}")
    print(f"- Расписаний: {GroupSchedule.objects.count()}")
    
    print(f"\nГруппы по уровням:")
    for level in LanguageLevel.objects.all():
        groups_count = Group.objects.filter(level=level).count()
        print(f"- {level.name}: {groups_count} групп")

if __name__ == '__main__':
    main()



