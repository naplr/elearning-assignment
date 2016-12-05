from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^1/$', views.first_video, name='first_video'),
    url(r'^2/$', views.first_reading, name='first_reading'),
    url(r'^3/$', views.first_quizzes, name='first_quizzes'),
    url(r'^4/$', views.second_video, name='second_video'),
    url(r'^5/$', views.second_reading, name='second_reading'),
    url(r'^6/$', views.second_quizzes, name='second_quizzes'),
    url(r'^7/$', views.interactive, name='interactive'),
    url(r'^done/$', views.done, name='done'),
]
