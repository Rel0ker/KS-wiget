from rest_framework import serializers
from .models import Application
from groups.serializers import GroupListSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    group = GroupListSerializer(read_only=True)
    group_id = serializers.IntegerField(write_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'name', 'email', 'phone', 'group', 'group_id',
            'comment', 'status', 'status_display', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Валидация данных"""
        from groups.models import Group
        
        # Проверяем существование группы
        try:
            group = Group.objects.get(pk=data['group_id'], is_active=True)
        except Group.DoesNotExist:
            raise serializers.ValidationError("Группа не найдена или неактивна")
        
        # Проверяем доступность мест
        if group.available_spots <= 0:
            raise serializers.ValidationError("В данной группе нет свободных мест")
        
        return data


class ApplicationCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заявки (виджет)"""
    group_id = serializers.IntegerField()
    
    class Meta:
        model = Application
        fields = ['name', 'email', 'phone', 'group_id', 'comment']
    
    def validate(self, data):
        """Валидация данных для создания заявки"""
        from groups.models import Group
        
        # Проверяем существование группы
        try:
            group = Group.objects.get(pk=data['group_id'], is_active=True)
        except Group.DoesNotExist:
            raise serializers.ValidationError("Группа не найдена или неактивна")
        
        # Проверяем доступность мест
        if group.available_spots <= 0:
            raise serializers.ValidationError("В данной группе нет свободных мест")
        
        return data
