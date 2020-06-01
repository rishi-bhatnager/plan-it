from django.shortcuts import render, redirect, reverse
from django.utils.html import format_html
from .models import Task
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

    return redirect(reverse('users:tasks'))
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
    fields = ['name', 'notes', 'category', 'dueDate', 'repeat', 'endRepeat', 'expTime']

    def form_valid(self, form):
        form.instance.user = self.request.user

        if form.cleaned_data['repeat'] == 'Never':
            Convert to UTC:
            form.instance.dueDateAll_set.add(form.cleaned_data['dueDate'])


            #Untested, maybe works, try if above fails
            # self.get_object().dueDateAll = form.cleaned_data['dueDate']

        else:
            from dateutil.relativedelta import relativedelta
            from datetime import datetime

            intervals = {
                'Daily': relativedelta(days=+1),
                'Weekly': relativedelta(weeks=+1),
                'Monthly': relativedelta(months=+1),
                'Yearly': relativedelta(years=+1),
            }

            lastDue = form.cleaned_data['dueDate']
            interval = intervals[form.cleaned_data['repeat']]
            nextDue = lastDue + interval
            endRepeat = form.cleaned_data['endRepeat']
            end = datetime(endRepeat.year, endRepeat.month, endRepeat.day, hour=23,minute=59,second=59,microsecond=999999)

            while nextDue < end:
#               ADD REPEATED DUE DATES HERE, Remember to CONVERT TO UTC



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
