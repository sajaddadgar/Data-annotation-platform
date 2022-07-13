from django.urls import path

from . import views

app_name = 'survey'

urlpatterns = [
    path('', views.home, name='home'),
    path('view', views.show_files, name='view'),
    path('vote', views.vote, name='vote'),
    # path('aaa', views.home2, name='home2'),
]