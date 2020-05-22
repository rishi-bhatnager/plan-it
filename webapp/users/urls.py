from django.urls import path, include, reverse_lazy
from django.views.generic import TemplateView
from . import views
from django.contrib.auth.views import PasswordResetConfirmView

app_name = 'users'
urlpatterns = [
    path('privacy-policy/', TemplateView.as_view(template_name='users/privacy_policy.html')),
    path('register/', views.register, name='register'),
    # path('', include('django.contrib.auth.urls')),                                                          django shortcut for all auth views
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('settings/', views.settings, name='settings'),
    path('change-password/', views.PasswordChangeView.as_view(success_url=reverse_lazy('planner:index')), name='change_password'),
    # path('password_change_done/', views.password_change_done, name='password_change_done'),
        # ^ not necessary rn bc successful password change set to redirect to home page
    path('password-reset/', views.PasswordResetView.as_view(success_url=reverse_lazy('users:password_reset_done')), name='password_reset'),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view( \
        success_url=reverse_lazy('users:login')), name='password_reset_confirm'),

    # see Authentication Views > Using the views in "Using the Django Authentication System" in Django docs
    # might need to add 'accounts/profile' to redirect successful logins

    # path('social/', include('allauth.urls')),                                                                         uncomment


    path('tasks/', views.TasksView.as_view(), name='tasks'),
    path('tasks/<int:pk>/', views.TaskDetailsView.as_view(), name='task_details'),
    path('tasks/<int:pk>/remove/', views.TaskRemoveView.as_view(), name='task_remove'),
    path('logout-login/', views.logout_login, name='logout_login'),
]
