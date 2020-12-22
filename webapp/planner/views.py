from django.shortcuts import render, redirect, reverse
from django.utils.html import format_html
from .models import Task, Event
from django.views.generic import CreateView, UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def index(request):
    if str(request.META.get('HTTP_REFERER')).endswith('users/change-password') \
        or str(request.META.get('HTTP_REFERER')).endswith('users/change-password/'):
            messages.success(request, f'Password successfully changed for {request.user.get_username()}')
    # if str(request.META.get('HTTP_REFERER')).endswith('/set-password') \
    #     or str(request.META.get('HTTP_REFERER')).endswith('/set-password/'):
    #         messages.success(request, f'Password successfully reset for {request.user.get_username()}')
        # ^ only uncomment if you can get users to stay logged in after resetting their password
            # (then also must redirect to home page instead of the login page as currently constructed)

    return redirect(reverse('users:settings'))
    #UNCOMMENT BELOW AND DELETE ABOVE ONCE NEW HOME PAGE IMPLEMENTED
    # return render(request, 'planner/index.html')

def sendToIndex(request):
    return redirect(reverse('planner:index'))

def unavailableFeature(request):
    return render(request, 'planner/unavailableFeature.html',
        {'title': 'Feature under Construction', 'redirect': request.META.get('HTTP_REFERER')})



class AddTaskView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'planner/add_task.html'
    model = Task
    fields = ['name', 'notes', 'category', 'dueDate', 'expTime']

    def form_valid(self, form):
        form.instance.user = self.request.user

        #Below doesn't work, but we should probably TRY TO IMPLEMENT AT SOME POINT
        # doesn't allow a task to be added if the user has another, equivalent task
        # NOTE: equivalence defined in models.py as same name, category, and dueDate
        # for other in self.request.user.task_set.all():
        #     if form.cleaned_data['name'] == other.name and form.cleaned_data['category'] == other.category \
        #         and form.cleaned_data['dueDate'] == other.dueDate:
        #             messages.error("You already have another task with the same name, category, and due date")
        #             return False

        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return format_html('task \"{}\" successfully added. <a href="{}">my tasks</a>', cleaned_data['name'], reverse('users:tasks'))

    def get_success_url(self):
        return reverse('planner:add_task')


class EditTaskView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    template_name = 'planner/edit_task.html'
    model = Task
    fields = ['name', 'notes', 'category', 'dueDate', 'expTime']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_success_message(self, cleaned_data):
        return 'task \"{}\" successfully edited'.format(cleaned_data['name'])

    def get_success_url(self):
        return reverse('users:task_details', kwargs={'pk': self.get_object().pk})




class AddEventView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'planner/add_event.html'
    model = Event
    fields = ['name', 'notes', 'startTime', 'duration']

    def form_valid(self, form):
        form.instance.user = self.request.user

        #Below doesn't work, but we should probably TRY TO IMPLEMENT AT SOME POINT
        ## Replace "task" with "event" below
        # doesn't allow a task to be added if the user has another, equivalent task
        # NOTE: equivalence defined in models.py as same name, category, and dueDate
        # for other in self.request.user.task_set.all():
        #     if form.cleaned_data['name'] == other.name and form.cleaned_data['category'] == other.category \
        #         and form.cleaned_data['dueDate'] == other.dueDate:
        #             messages.error("You already have another task with the same name, category, and due date")
        #             return False

        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return format_html('event \"{}\" successfully added. <a href="{}">my events</a>', cleaned_data['name'], reverse('users:events'))

    def get_success_url(self):
        return reverse('planner:add_event')


class EditEventView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    template_name = 'planner/edit_event.html'
    model = Event
    fields = ['name', 'notes', 'startTime', 'duration']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_success_message(self, cleaned_data):
        return 'event \"{}\" successfully edited'.format(cleaned_data['name'])

    def get_success_url(self):
        return reverse('users:event_details', kwargs={'pk': self.get_object().pk})
