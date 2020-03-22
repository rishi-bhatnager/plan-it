from django.urls import path, include
from django.views.generic import TemplateView
# from django.contrib.auth import views
from . import views

app_name = 'users'
urlpatterns = [
    path('privacy_policy', TemplateView.as_view(template_name='users/privacy_policy.html')),
    path('register', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),
        # ^ creates default URLs for login, logout, password change, etc
            # can create custom views by not using shortcut and subclassing the default views
                # see Authentication Views > Using the views in "Using the Django Authentication System" in Django docs

                                                                                                                        # might need to add 'accounts/profile' to
                                                                                                                        # redirect successful logins
    # path('social/', include('allauth.urls')),                                                                         uncomment
]
