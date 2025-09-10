from django.contrib import admin
from django.utils.html import format_html
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'email', 'phone', 'group', 'status', 
        'created_at', 'status_color'
    ]
    list_filter = ['status', 'group', 'created_at']
    search_fields = ['name', 'email', 'phone', 'comment']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'email', 'phone', 'group')
        }),
        ('Детали', {
            'fields': ('comment', 'status')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_color(self, obj):
        """Цветовая индикация статуса"""
        colors = {
            'new': '#FFA500',      # Оранжевый
            'processed': '#008000', # Зеленый
            'rejected': '#FF0000',  # Красный
        }
        color = colors.get(obj.status, '#000000')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_color.short_description = 'Статус'
    
    def save_model(self, request, obj, form, change):
        """Логирование изменений статуса"""
        if change and 'status' in form.changed_data:
            old_instance = Application.objects.get(pk=obj.pk)
            old_status = old_instance.status
            new_status = obj.status
            
            # Логируем изменение статуса
            print(f"Заявка {obj.id}: статус изменен с '{old_status}' на '{new_status}'")
            
            # Здесь можно добавить уведомления в Telegram
            if new_status == 'new':
                self.send_telegram_notification(obj)
        
        super().save_model(request, obj, form, change)
    
    def send_telegram_notification(self, application):
        """Отправка уведомления в Telegram (заглушка)"""
        # TODO: Реализовать интеграцию с Telegram Bot API
        pass
