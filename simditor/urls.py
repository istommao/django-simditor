"""simditor urls."""
from __future__ import absolute_import

import django
from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from . import views

if django.VERSION >= (1, 8):
    # pylint disable=C0103
    urlpatterns = [
        url(r'^upload/', staff_member_required(views.UPLOAD),
            name='simditor_upload'),
    ]
else:
    from django.conf.urls import patterns    # pylint disable=C0411

    # pylint disable=C0103
    urlpatterns = patterns(
        '',
        url(r'^upload/', staff_member_required(views.UPLOAD),
            name='simditor_upload'),
    )
