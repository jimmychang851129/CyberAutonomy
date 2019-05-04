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
from CPAnalysis.views import CPHome_page,CP_Request
from HSTSAnalysis.views import HSTSHome_page,HSTS_Request
from CAAnalysis.views import CAHome_page, CA_Request,CADetail
from HTTPSAnalysis.views import HTTPSHome_page, HTTPS_Request
from TLSAnalysis.views import TLSHome_page, TLS_Request, OverallTLSDetail
from testApp.views import testHttpsApp,testHSTSApp,testTLSApp,testCAApp

# with name parameter, we can refer to it by name rather than url
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('home',home_page,name='home'),	# name parameter is used as a variable, other program called it by this name
    path('CPAnalysis',CPHome_page,name='CP'),
    path('HSTSAnalysis',HSTSHome_page,name='HSTSAnalysis'),
    path('CAAnalysis',CAHome_page,name='CAAnalysis'),
    path('HTTPSAnalysis',HTTPSHome_page,name='HTTPSAnalysis'),
    path('TLSAnalysis',TLSHome_page,name='TLSAnalysis'),
    path('HTTPS_Request',HTTPS_Request,name='HTTPS_Request'),
    path('HSTS_Request',HSTS_Request,name='HSTS_Request'),
    path('TLS_Request',TLS_Request,name='TLS_Request'),
    path('CA_Request',CA_Request,name='CA_Request'),
    path('CP_Request',CP_Request,name='CP_Request'),
    path('CADetail',CADetail,name='CADetail'),
    path('OverallTLSDetail',OverallTLSDetail,name='OverallTLSDetail'),
    # path('HTTPSHSTSDetail',HTTPSHSTSDetail,name='HTTPSHSTSDetail'),
    path('testHttps',testHttpsApp,name='testHttps'),
    path('testHSTS',testHSTSApp,name='testHSTS'),
    path('testTLS',testTLSApp,name='testTLS'),
    path('testCAApp',testCAApp,name='testCAApp'),

]