"""
URL configuration for LMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import settings
from .home_view import signin, signup, homeadmin, viewusers, profile, deluser, signout, start, editpro

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Books.urls')),
    path('', include('USERS.urls')),
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('hadmin/', homeadmin, name='homeadmin'),
    path('viewusers/', viewusers, name='viewusers'),
    path('profile/', profile, name= 'profile'),
    path('deluser/<int:id>/', deluser, name="deluser"),
    path('signout/', signout, name='signout'),
    path('', start, name='start'),
    path('editpro', editpro, name='editpro'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='home/password_reset.html'), name= 'password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='home/password_reset_done.html'), name= 'password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='home/password_reset_confirm.html'), name= 'password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='home/password_reset_complete.html'), name= 'password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
