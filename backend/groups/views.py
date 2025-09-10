from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import LanguageLevel, Group, DayOfWeek, TimeSlot
from .serializers import (
    LanguageLevelSerializer, GroupSerializer, GroupListSerializer,
    DayOfWeekSerializer, TimeSlotSerializer
)


class LanguageLevelViewSet(viewsets.ReadOnlyModelViewSet):
    """API для уровней языка"""
    queryset = LanguageLevel.objects.all()
    serializer_class = LanguageLevelSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'name']
    ordering = ['order']


class DayOfWeekViewSet(viewsets.ReadOnlyModelViewSet):
    """API для дней недели"""
    queryset = DayOfWeek.objects.all()
    serializer_class = DayOfWeekSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'name']
    ordering = ['order']


class TimeSlotViewSet(viewsets.ReadOnlyModelViewSet):
    """API для временных слотов"""
    queryset = TimeSlot.objects.filter(is_active=True)
    serializer_class = TimeSlotSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['start_time', 'end_time']
    ordering = ['start_time']


class GroupViewSet(viewsets.ModelViewSet):
    """API для групп (только для администраторов)"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['level', 'is_active', 'color']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'total_capacity', 'available_spots', 'level__name', 'level__order']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Фильтрация по активным группам для не-администраторов"""
        if self.action == 'list' and not self.request.user.is_staff:
            return Group.objects.filter(is_active=True)
        return Group.objects.all()
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def public(self, request):
        """Публичный API для виджета (только активные группы с местами)"""
        groups = Group.objects.filter(
            is_active=True
        ).select_related('level')
        
        # Фильтрация по уровню
        level_id = request.query_params.get('level')
        if level_id:
            groups = groups.filter(level_id=level_id)
        
        # Только группы с доступными местами
        groups = [group for group in groups if group.available_spots > 0]
        
        # Сортировка
        sort_by = request.query_params.get('sort', 'name')
        if sort_by == 'available_spots':
            groups.sort(key=lambda x: x.available_spots, reverse=True)
        elif sort_by == 'level':
            groups.sort(key=lambda x: (x.level.order, x.name))
        else:
            groups.sort(key=lambda x: x.name)
        
        serializer = GroupListSerializer(groups, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def details(self, request, pk=None):
        """Детальная информация о группе для виджета"""
        try:
            group = Group.objects.get(pk=pk, is_active=True)
            serializer = GroupListSerializer(group)
            return Response(serializer.data)
        except Group.DoesNotExist:
            return Response({'error': 'Группа не найдена'}, status=404)
