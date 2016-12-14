"""Noisemakers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from influencers.views import HomeViews
from django.conf.urls.static import static
from django.contrib import admin
from . import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeViews.as_view(), name='index'),
    url(r'^influencers/', include('influencers.urls')),
    url(r'^noisemaker_invite/', include('noisemaker_invite.urls'), name='noisemaker_invite'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
 
