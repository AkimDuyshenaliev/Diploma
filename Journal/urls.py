from django.contrib import admin
from django.urls import include, path, re_path

from django.conf import settings
from django.conf.urls.static import static

from .views import *

app_name = 'Journal'
urlpatterns = [
    path('', MainPageView.as_view(), name='MainPage'),
    re_path(r'^group/(?P<group_slug>[\w-]+)/$', GroupPageView.as_view(), name='GroupPage'),
    re_path(r'^group/(?P<group_slug>[\w-]+)/(?P<subject>[\w-]+)/$', JournalPageView.as_view(), name='JournalPage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
