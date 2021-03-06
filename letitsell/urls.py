"""letitsell URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from home import views


urlpatterns = [
    url(r'^$', views.greeting_page, name='greeting_page'),
    url(r'^sign/$', views.sign_in_page, name='sign_in_page'),
    url(r'^profile/$', views.profile_page, name='profile_page'),
    url(r'^mailing/$', views.send_email, name='send_email'),
    url(r'^polls/', include('polls.urls', namespace='polls')),
    url(r'^shop/', include('shop.urls', namespace='shop')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^users/', include('userprofiles.urls', namespace="users")),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT
                          )
