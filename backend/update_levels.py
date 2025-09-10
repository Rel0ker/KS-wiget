#!/usr/bin/env python
"""
Скрипт для обновления уровней языков
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ks_widget.settings_production')
django.setup()

from groups.models import LanguageLevel, Group

def update_levels():
    """Обновление уровней языков"""
    
    # Удаляем все существующие уровни
    print("Удаление старых уровней...")
    LanguageLevel.objects.all().delete()
    
    # Создаем новые уровни
    levels_data = [
        {'name': 'Начинающие', 'order': 1, 'description': 'Для начинающих изучать корейский язык'},
        {'name': 'Средний уровень', 'order': 2, 'description': 'Средний уровень владения корейским языком'},
        {'name': 'Продвинутые', 'order': 3, 'description': 'Продвинутый уровень корейского языка'},
    ]
    
    new_levels = {}
    for level_data in levels_data:
        level = LanguageLevel.objects.create(**level_data)
        new_levels[level_data['name']] = level
        print(f"Создан уровень: {level.name}")

def update_groups():
    """Обновление групп с новыми уровнями"""
    
    # Получаем новые уровни
    levels = LanguageLevel.objects.all()
    level_map = {level.name: level for level in levels}
    
    # Маппинг старых уровней на новые
    old_to_new = {
        'Начальный': 'Начинающие',
        'Элементарный': 'Начинающие', 
        'Средний': 'Средний уровень',
        'Продвинутый': 'Продвинутые',
        'Высший': 'Продвинутые'
    }
    
    # Обновляем группы
    groups = Group.objects.all()
    for group in groups:
        old_level_name = group.level.name
        new_level_name = old_to_new.get(old_level_name, 'Начинающие')
        new_level = level_map[new_level_name]
        
        group.level = new_level
        group.save()
        print(f"Обновлена группа '{group.name}': {old_level_name} -> {new_level_name}")

def main():
    print("Обновление уровней языков...")
    print("=" * 50)
    
    print("\n1. Обновление уровней...")
    update_levels()
    
    print("\n2. Обновление групп...")
    update_groups()
    
    print("\n" + "=" * 50)
    print("Обновление завершено!")
    
    # Выводим статистику
    print(f"\nСтатистика:")
    print(f"- Уровней языков: {LanguageLevel.objects.count()}")
    print(f"- Групп: {Group.objects.count()}")
    
    print(f"\nУровни:")
    for level in LanguageLevel.objects.all():
        groups_count = Group.objects.filter(level=level).count()
        print(f"- {level.name}: {groups_count} групп")

if __name__ == '__main__':
    main()



