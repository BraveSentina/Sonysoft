"""apparel_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include
from .views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homepage_page,name='homepage_page'),
    path('about/',about_page,name='about_page'),
    path('terms/',terms_page,name='terms_page'),
    path('do_login/',login_page,name='login_page'),
    path('register/',register_page,name='register_page'),
    path('register_success/',register_success_page,name='register_success_page'),

    path('do_logout/',do_logout,name='do_logout'),

    path('student/',include('student.urls')),
    path('administrator/',include('administrator.urls')),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)