from django.urls import path, include
from django.views.generic import TemplateView

from . import views

app_name = 'planner'
urlpatterns = [
    path('index.html', views.IndexView.as_view(), name='index'),
    path('', views.IndexView.as_view(), name='index'),
    path('privacy_policy', TemplateView.as_view(template_name='planner/privacy_policy.html')),
    path('accounts/', include('django.contrib.auth.urls')),
]
