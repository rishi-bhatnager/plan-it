from django.shortcuts import render, redirect, reverse
from .models import Task
from django.contrib import messages

def index(request):
    if str(request.META.get('HTTP_REFERER')).endswith('users/change-password') \
        or str(request.META.get('HTTP_REFERER')).endswith('users/change-password/'):
            messages.success(request, f'Password successfully changed for {request.user.get_username()}')
    # if str(request.META.get('HTTP_REFERER')).endswith('/set-password') \
    #     or str(request.META.get('HTTP_REFERER')).endswith('/set-password/'):
    #         messages.success(request, f'Password successfully reset for {request.user.get_username()}')
        # ^ only uncomment if you can get users to stay logged in after resetting their password
            # (then also must redirect to home page instead of the login page as currently constructed)
    return render(request, 'planner/index.html')

def sendToIndex(request):
    return redirect(reverse('planner:index'))

def unavailableFeature(request):
    return render(request, 'planner/unavailableFeature.html',
        {'title': 'Feature under Construction', 'redirect': request.META.get('HTTP_REFERER')})
