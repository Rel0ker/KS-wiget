from rest_framework import serializers
from .models import LanguageLevel, Group, DayOfWeek, TimeSlot


class LanguageLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageLevel
        fields = ['id', 'name', 'description', 'order']


class DayOfWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayOfWeek
        fields = ['id', 'name', 'order']


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'start_time', 'end_time', 'is_active']


class GroupSerializer(serializers.ModelSerializer):
    level = LanguageLevelSerializer(read_only=True)
    level_id = serializers.IntegerField(write_only=True)
    available_spots = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    
    class Meta:
        model = Group
        fields = [
            'id', 'name', 'level', 'level_id', 'total_capacity', 
            'current_participants', 'available_spots', 'color', 
            'description', 'start_date', 'schedule', 'is_active',
            'is_full', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Валидация данных"""
        if 'total_capacity' in data and 'current_participants' in data:
            if data['current_participants'] > data['total_capacity']:
                raise serializers.ValidationError(
                    "Текущее количество участников не может превышать общее количество"
                )
        return data


class GroupListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка групп (виджет)"""
    level = LanguageLevelSerializer(read_only=True)
    available_spots = serializers.ReadOnlyField()
    schedule = serializers.SerializerMethodField()
    
    class Meta:
        model = Group
        fields = [
            'id', 'name', 'level', 'total_capacity', 'available_spots',
            'color', 'description', 'start_date', 'schedule'
        ]
    
    def get_schedule(self, obj):
        """Получить расписание в формате для виджета"""
        return obj.get_schedule_for_widget()
