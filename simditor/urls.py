"""simditor urls."""
from __future__ import absolute_import

import django

from django.conf import settings
from django.conf.urls import static
from django.contrib.admin.views.decorators import staff_member_required

from . import views

if django.VERSION >= (2, 0):
    # pylint disable=C0103
    from django.urls import re_path
    urlpatterns = [
        re_path('upload[/]{0,1}', staff_member_required(views.UPLOAD),
             name='simditor_upload'),
    ]
elif django.VERSION >= (1, 8):
    from django.conf.urls import url
    # pylint disable=C0103
    urlpatterns = [
        url(r'^upload[/]{0,1}', staff_member_required(views.UPLOAD),
            name='simditor_upload'),
    ]
else:
    from django.conf.urls import patterns, url    # pylint disable=C0411
    # pylint disable=C0103
    urlpatterns = patterns(
        '',
        url(r'^upload[/]{0,1}', staff_member_required(views.UPLOAD),
            name='simditor_upload'),
    )

if settings.DEBUG:
    urlpatterns += static.static(settings.MEDIA_URL,
                                 document_root=settings.MEDIA_ROOT)
    urlpatterns += static.static(settings.STATIC_URL,
                                 document_root=settings.STATIC_ROOT)
