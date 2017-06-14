"""simditor image_processing."""
from __future__ import absolute_import

from django.conf import settings


def get_backend():
    """Get backend."""
    backend = getattr(settings, 'SIMDITOR_IMAGE_BACKEND', None)

    if backend == 'pillow':
        from simditor.image import pillow_backend as backend
    else:
        from simditor.image import dummy_backend as backend
    return backend
