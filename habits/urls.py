from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # Calendar entries
    path('entries/create/', views.create_calendar_entry, name='create_calendar_entry'),
    path('entries/<int:pk>/rename/', views.rename_calendar_entry, name='rename_calendar_entry'),
]