from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
import json


class LanguageLevel(models.Model):
    """Уровень знания корейского языка"""
    name = models.CharField(_('Название'), max_length=50, unique=True)
    description = models.TextField(_('Описание'), blank=True)
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    
    class Meta:
        verbose_name = _('Уровень языка')
        verbose_name_plural = _('Уровни языка')
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class DayOfWeek(models.Model):
    """Дни недели"""
    DAY_CHOICES = [
        ('monday', _('Понедельник')),
        ('tuesday', _('Вторник')),
        ('wednesday', _('Среда')),
        ('thursday', _('Четверг')),
        ('friday', _('Пятница')),
        ('saturday', _('Суббота')),
        ('sunday', _('Воскресенье')),
    ]
    
    name = models.CharField(_('Название'), max_length=20, choices=DAY_CHOICES, unique=True)
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    
    class Meta:
        verbose_name = _('День недели')
        verbose_name_plural = _('Дни недели')
        ordering = ['order']
    
    def __str__(self):
        return str(dict(self.DAY_CHOICES)[self.name])


class TimeSlot(models.Model):
    """Временные слоты для занятий"""
    start_time = models.TimeField(_('Время начала'))
    end_time = models.TimeField(_('Время окончания'))
    is_active = models.BooleanField(_('Активен'), default=True)
    
    class Meta:
        verbose_name = _('Временной слот')
        verbose_name_plural = _('Временные слоты')
        ordering = ['start_time']
        unique_together = ['start_time', 'end_time']
    
    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


class GroupSchedule(models.Model):
    """Расписание группы"""
    group = models.ForeignKey(
        'Group', 
        on_delete=models.CASCADE, 
        verbose_name=_('Группа'),
        related_name='schedules'
    )
    day_of_week = models.ForeignKey(
        DayOfWeek, 
        on_delete=models.CASCADE, 
        verbose_name=_('День недели')
    )
    time_slot = models.ForeignKey(
        TimeSlot, 
        on_delete=models.CASCADE, 
        verbose_name=_('Временной слот')
    )
    is_active = models.BooleanField(_('Активно'), default=True)
    
    class Meta:
        verbose_name = _('Расписание группы')
        verbose_name_plural = _('Расписания групп')
        unique_together = ['group', 'day_of_week', 'time_slot']
        ordering = ['day_of_week__order', 'time_slot__start_time']
    
    def __str__(self):
        return f"{self.group.name} - {self.day_of_week} {self.time_slot}"


class Group(models.Model):
    """Группа для изучения корейского языка"""
    name = models.CharField(_('Название группы'), max_length=200)
    level = models.ForeignKey(
        LanguageLevel, 
        on_delete=models.CASCADE, 
        verbose_name=_('Уровень знания'),
        related_name='groups'
    )
    total_capacity = models.PositiveIntegerField(
        _('Общее количество участников'),
        validators=[MinValueValidator(1)]
    )
    current_participants = models.PositiveIntegerField(
        _('Текущее количество участников'),
        default=0,
        validators=[MinValueValidator(0)]
    )
    color = models.CharField(_('Цвет группы'), max_length=7, default='#3B82F6')
    description = models.TextField(_('Подробное описание'), blank=True)
    start_date = models.DateField(_('Дата начала'), null=True, blank=True)
    schedule = models.TextField(_('Расписание'), blank=True)
    is_active = models.BooleanField(_('Активна'), default=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)
    
    class Meta:
        verbose_name = _('Группа')
        verbose_name_plural = _('Группы')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.level.name})"
    
    @property
    def available_spots(self):
        """Количество доступных мест"""
        return max(0, self.total_capacity - self.current_participants)
    
    @property
    def is_full(self):
        """Группа заполнена"""
        return self.available_spots == 0
    
    def get_schedule_display(self):
        """Получить расписание в читаемом виде"""
        schedules = self.schedules.filter(is_active=True).select_related('day_of_week', 'time_slot')
        if not schedules.exists():
            return self.schedule  # Fallback на старое поле
        
        schedule_dict = {}
        for schedule in schedules:
            day_name = schedule.day_of_week.get_name_display()
            time_str = str(schedule.time_slot.start_time)[:5]  # HH:MM
            if day_name not in schedule_dict:
                schedule_dict[day_name] = []
            schedule_dict[day_name].append(time_str)
        
        # Формируем строку расписания
        schedule_parts = []
        for day, times in schedule_dict.items():
            times_str = ', '.join(times)
            schedule_parts.append(f"{day} {times_str}")
        
        return '; '.join(schedule_parts)
    
    def get_schedule_for_widget(self):
        """Получить расписание в формате для виджета"""
        schedules = self.schedules.filter(is_active=True).select_related('day_of_week', 'time_slot')
        if not schedules.exists():
            return self.schedule  # Fallback на старое поле
        
        schedule_dict = {}
        for schedule in schedules:
            day_key = schedule.day_of_week.name  # monday, tuesday, etc.
            time_str = str(schedule.time_slot.start_time)[:5]  # HH:MM
            if day_key not in schedule_dict:
                schedule_dict[day_key] = []
            schedule_dict[day_key].append(time_str)
        
        return schedule_dict
    
    def save(self, *args, **kwargs):
        # Проверяем, что текущее количество не превышает общее
        if self.current_participants > self.total_capacity:
            self.current_participants = self.total_capacity
        super().save(*args, **kwargs)
