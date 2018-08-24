"""simditor_demo URL Configuration

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
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from app.views import IndexView

from simditor.views import upload_handler


class ImageUploadView(generic.View):
    """ImageUploadView."""

    http_method_names = ['post']

    def post(self, request, **kwargs):
        """Post."""
        return upload_handler(request)


# pylint disable=C0103
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='simditor-form'),
    url(r'^admin/', admin.site.urls),
    url(r'^simditor/upload', csrf_exempt(ImageUploadView.as_view())),
]

urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
