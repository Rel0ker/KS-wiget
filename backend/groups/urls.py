from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LanguageLevelViewSet, GroupViewSet, DayOfWeekViewSet, TimeSlotViewSet

router = DefaultRouter()
router.register(r'levels', LanguageLevelViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'days', DayOfWeekViewSet)
router.register(r'timeslots', TimeSlotViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
