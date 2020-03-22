from django.shortcuts import render, redirect, reverse
from .models import UserRegistrationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for {username}')
            return redirect(reverse('planner:index'))
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'plan it - create account'})
