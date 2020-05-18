from django.shortcuts import render, redirect, reverse
from .models import UserRegistrationForm
from django.apps import apps
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth import views, login, authenticate
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            login(request, authenticate(username=username, password=form.cleaned_data.get('password1')))
            messages.success(request, f'Account successfully created for {username}. You are now logged in.')
            return redirect(reverse('planner:index'))
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'plan it - create account'})



class LoginView(views.LoginView):
    # form = AuthenticationForm()

    def get(self, request, template_name='registration/login.html'):
        if str(request.META.get('HTTP_REFERER')).endswith('/set-password') \
            or str(request.META.get('HTTP_REFERER')).endswith('/set-password/'):
                messages.success(request, f'Password successfully reset. Please log in using your new password.')

        self.redirect_field_name = template_name
        return render(request, template_name, {'form': self.form_class, 'title': 'plan it - login'})



class LogoutView(views.LogoutView):
    def get(self, request, template_name='registration/logged_out.html'):
        return render(request, template_name, {'title': 'plan it - logged out successfully'})


@login_required
def settings(request):
    return render(request, 'users/settings.html', {'title': f'{request.user.username} - settings'})


class PasswordChangeView(views.PasswordChangeView):
    def get(self, request, template_name = 'registration/password_change_form.html'):
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)

            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                login(request, authenticate(username=username, password=form.cleaned_data.get('password1')))
                return success_url
        else:
            form = PasswordChangeForm(request.user)
        return render(request, template_name, {'form': form, 'title': 'change password'})


# @login_required
# def password_change_done(request):
#     return redirect(reverse('planner:index'))


class PasswordResetView(views.PasswordResetView):
    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class, 'title': 'reset password'})


class PasswordResetDoneView(views.PasswordResetDoneView):
    def get(self, request):
        return render(request, self.template_name, {'title': 'password reset confirmation'})

# class PasswordResetConfirmView(views.PasswordResetConfirmView):
#     def get(self, request, **kwargs):
#         breakpoint()
#         if request.method == 'POST':
#             form = SetPasswordForm(request.user, request.POST)
#             breakpoint()

#             if form.is_valid():
#                 breakpoint()
#                 form.save()
#                 update_session_auth_hash(request, form.user)
#                 login(request, authenticate(username=username, password=form.cleaned_data.get('new_password1')))
#                 return success_url
#         else:
#             form = SetPasswordForm(request.user)
#         return render(request, self.template_name, {'form': form, 'title': 'set new password'})



class TasksView(ListView):
    Task = apps.get_model('planner', 'Task')
    model = Task
    context_object_name = 'tasks'
