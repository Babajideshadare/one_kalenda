from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    # Profile
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Calendar entries
    path('entries/create/', views.create_calendar_entry, name='create_calendar_entry'),
    path('entries/<int:pk>/rename/', views.rename_calendar_entry, name='rename_calendar_entry'),
]