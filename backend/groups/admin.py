from django.contrib import admin
from django.utils.html import format_html
from django.forms import ModelForm, CheckboxSelectMultiple, SelectMultiple, TimeInput
from django.db import models
from django import forms
from .models import LanguageLevel, Group, DayOfWeek, TimeSlot, GroupSchedule


@admin.register(LanguageLevel)
class LanguageLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'description']
    list_editable = ['order']
    search_fields = ['name']
    ordering = ['order', 'name']


@admin.register(DayOfWeek)
class DayOfWeekAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']
    search_fields = ['name']
    ordering = ['order']


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'end_time', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active']
    search_fields = ['start_time', 'end_time']
    ordering = ['start_time']


class GroupScheduleInline(admin.TabularInline):
    model = GroupSchedule
    extra = 0
    fields = ['day_of_week', 'time_slot', 'is_active']
    autocomplete_fields = ['day_of_week', 'time_slot']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'level', 'total_capacity', 'current_participants', 
        'available_spots', 'color_preview', 'is_active', 'created_at'
    ]
    list_filter = ['level', 'is_active', 'start_date', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'current_participants']
    readonly_fields = ['available_spots', 'created_at', 'updated_at', 'schedule_display']
    inlines = [GroupScheduleInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'level', 'is_active')
        }),
        ('Вместимость', {
            'fields': ('total_capacity', 'current_participants', 'available_spots')
        }),
        ('Внешний вид', {
            'fields': ('color', 'description')
        }),
        ('Расписание', {
            'fields': ('schedule_display',),
            'classes': ('collapse',)
        }),
        ('Дополнительно', {
            'fields': ('start_date', 'schedule'),
            'classes': ('collapse',)
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def color_preview(self, obj):
        """Предварительный просмотр цвета"""
        if obj.color:
            return format_html(
                '<div style="background-color: {}; width: 30px; height: 20px; border: 1px solid #ccc; border-radius: 3px;" title="{}"></div>',
                obj.color, obj.color
            )
        return '-'
    color_preview.short_description = 'Цвет'
    
    def available_spots(self, obj):
        """Количество доступных мест"""
        return obj.available_spots
    available_spots.short_description = 'Доступно мест'
    
    def schedule_display(self, obj):
        """Отображение расписания в админке"""
        if obj.pk:
            return obj.get_schedule_display()
        return "Сначала сохраните группу, затем добавьте расписание"
    schedule_display.short_description = 'Текущее расписание'
    
    def save_model(self, request, obj, form, change):
        """Автоматический пересчет доступных мест"""
        if change and 'total_capacity' in form.changed_data:
            # Если изменили общее количество, пересчитываем доступные места
            if obj.current_participants > obj.total_capacity:
                obj.current_participants = obj.total_capacity
        super().save_model(request, obj, form, change)
