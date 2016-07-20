"""microblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from common.views import index

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    # api urls
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-accounts/', include('accounts_rest.urls', namespace="accounts_rest")),
    url(r'^api-microblogs/', include("blogs_rest.urls", namespace="blogs_rest")),
    # regular http urls
    url(r'^admin/', admin.site.urls),
    url(r'^index/$|^$', index, name='index'),
    url(r'^microblogs/', include('blogs.urls', namespace="microblogs")),
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),
]
