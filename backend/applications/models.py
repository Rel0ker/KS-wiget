from django.db import models
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _
from groups.models import Group


class Application(models.Model):
    """Заявка на участие в группе"""
    STATUS_CHOICES = [
        ('new', _('Новая')),
        ('processed', _('Обработанная')),
        ('rejected', _('Отклоненная')),
    ]
    
    name = models.CharField(_('Имя пользователя'), max_length=100)
    email = models.EmailField(_('Email'), validators=[EmailValidator()])
    phone = models.CharField(_('Телефон'), max_length=20, blank=True)
    group = models.ForeignKey(
        Group, 
        on_delete=models.CASCADE, 
        verbose_name=_('Выбранная группа'),
        related_name='applications'
    )
    comment = models.TextField(_('Комментарий'), blank=True)
    status = models.CharField(
        _('Статус'), 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='new'
    )
    created_at = models.DateTimeField(_('Дата подачи'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)
    
    class Meta:
        verbose_name = _('Заявка')
        verbose_name_plural = _('Заявки')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.group.name} ({self.get_status_display()})"
    
    def save(self, *args, **kwargs):
        """Автоматическое обновление количества участников при изменении статуса"""
        if self.pk:  # Если это обновление существующей заявки
            old_instance = Application.objects.get(pk=self.pk)
            old_status = old_instance.status
            new_status = self.status
            
            # Если статус изменился с 'new' на 'processed'
            if old_status == 'new' and new_status == 'processed':
                self.group.current_participants += 1
                self.group.save()
            # Если статус изменился с 'processed' на другой
            elif old_status == 'processed' and new_status != 'processed':
                if self.group.current_participants > 0:
                    self.group.current_participants -= 1
                    self.group.save()
        
        super().save(*args, **kwargs)
