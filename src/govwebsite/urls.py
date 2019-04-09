"""govwebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path

from homepage.views import home_page # from app import views.py
from CPAnalysis.views import CPHome_page,CPDate

# with name parameter, we can refer to it by name rather than url
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',home_page,name='home'),	# name parameter is used as a variable, other program called it by this name
    path('CPAnalysis',CPHome_page,name='CP'),
    path('CPDate',CPDate,name='CPDate')
]