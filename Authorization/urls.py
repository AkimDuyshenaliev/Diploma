from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path(r'search-result/$', search, name='search'),
    path('register', register, name='register'),
    path('login', auth_views.LoginView.as_view(template_name='Authorization/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='Authorization/logout.html'), name='logout'),
    path('profile', profile, name='profile'),
    path('allUsers', AllUsersView.as_view(template_name='Authorization/allUsers.html'), name='allUsers'),
    path('allSubjects', AllSubjectsView.as_view(template_name='Authorization/allSubjects.html'), name='allSubjects'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
