from django.urls import path

from measurement.views import SensorsView, OneSensorView, TempAdd

urlpatterns = [
    path('sensors/', SensorsView.as_view()),
    path('sensors/<pk>/', OneSensorView.as_view()),
    path('measurements/', TempAdd.as_view())

]
