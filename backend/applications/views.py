from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Application
from .serializers import ApplicationSerializer, ApplicationCreateSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    """API для заявок"""
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'group', 'created_at']
    search_fields = ['name', 'email', 'phone']
    ordering_fields = ['created_at', 'name', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Фильтрация по пользователю для не-администраторов"""
        if not self.request.user.is_staff:
            return Application.objects.filter(email=self.request.user.email)
        return Application.objects.all()
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def create_public(self, request):
        """Публичный API для создания заявки (виджет)"""
        serializer = ApplicationCreateSerializer(data=request.data)
        if serializer.is_valid():
            application = serializer.save()
            
            # Возвращаем успешный ответ
            return Response({
                'message': 'Заявка отправлена',
                'application_id': application.id
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def change_status(self, request, pk=None):
        """Изменение статуса заявки"""
        try:
            application = self.get_object()
            new_status = request.data.get('status')
            
            if new_status not in dict(Application.STATUS_CHOICES):
                return Response(
                    {'error': 'Неверный статус'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            application.status = new_status
            application.save()
            
            return Response({
                'message': f'Статус изменен на {application.get_status_display()}',
                'status': new_status
            })
            
        except Application.DoesNotExist:
            return Response(
                {'error': 'Заявка не найдена'}, 
                status=status.HTTP_404_NOT_FOUND
            )
