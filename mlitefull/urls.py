"""mlitefull URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from accounts.views import register, ajax_test, ajaxresponse, sendinbox
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(extra_context={'title': 'Đăng nhập'}), name='login'),
    path('logout/', LogoutView.as_view(extra_context={'title': 'Đăng Xuất'}, template_name='registration/logout.html'), name='logout'),
    path('', include('pagetools.urls')),
    path('ajaxtest/', ajax_test),
    path('ajaxresponse/', ajaxresponse, name='ajaxresponse'),
    path('sendinbox/', sendinbox, name='sendinbox')
]
