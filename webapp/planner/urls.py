from django.urls import path, include

from . import views

app_name = 'planner'
urlpatterns = [
    path('index.html', views.IndexView.as_view(), name='index'),
    path('', views.IndexView.as_view(), name='index'),
]
