from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('entries/create/', views.create_calendar_entry, name='create_calendar_entry'),
    path('entries/<int:pk>/rename/', views.rename_calendar_entry, name='rename_calendar_entry'),
]