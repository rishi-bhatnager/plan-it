from django.urls import path, include

from . import views

app_name = 'planner'
urlpatterns = [
    path('index.html', views.sendToIndex, name='indexRedirect'),
    path('', views.index, name='index'),
    path('feature-unavailable/', views.unavailableFeature, name='feature-unavailable'),
]
