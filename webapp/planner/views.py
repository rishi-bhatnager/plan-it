from django.shortcuts import render, redirect, reverse
from .models import Task
from django.views.generic import CreateView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

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



class AddTaskView(LoginRequiredMixin, CreateView):
    template_name = 'planner/add_task.html'
    model = Task
    fields = ['name', 'notes', 'category', 'dueDate', 'expTime']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('planner:add_task')


class EditTaskView(LoginRequiredMixin, UpdateView):
    template_name = 'planner/edit_task.html'
    model = Task
    fields = ['name', 'notes', 'category', 'dueDate', 'expTime']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:task_details', kwargs={'pk': self.get_object().pk})
