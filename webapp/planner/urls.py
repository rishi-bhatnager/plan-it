from django.urls import path, include

from . import views

app_name = 'planner'
urlpatterns = [
    path('index.html/', views.sendToIndex, name='indexRedirect'),
    path('', views.index, name='index'),
    path('feature-unavailable/', views.unavailableFeature, name='feature-unavailable'),
    path('task/add/', views.AddTaskView.as_view(), name='add_task'),
    path('task/edit/<int:pk>/', views.EditTaskView.as_view(), name='edit_task'),
]
