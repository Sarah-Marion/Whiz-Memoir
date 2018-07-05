"""whiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
import memoir.views as app_views
from memoir.forms import LoginForm, SignUpForm
from django.conf import settings
from django.conf.urls.static import static
from .views import index
from memoir.models import Task

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('memoir.urls')),
    url(r'^login/$', views.login, {'template_name': 'registration/login.html',
                                   "authentication_form": LoginForm}, name='login'),
    url(r'^signup/$', app_views.signup, name='signup'),
    url(r'^account_activation_sent/$', app_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        app_views.activate, name='activate'),
    url(r'^logout/$', views.logout, {'next_page': 'login'}, name='logout'),    
    url(r'^$', app_views.index, name="index"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
