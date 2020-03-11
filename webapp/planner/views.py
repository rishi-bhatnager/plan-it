from django.shortcuts import render
from django.views.generic import base
from .models import Task

class IndexView(base.TemplateView):
    template_name = 'planner/index.html'
