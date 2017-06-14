"""simditor image pillow_backend."""
from __future__ import absolute_import

import os
from io import BytesIO

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile

from simditor import utils

try:
    from PIL import Image, ImageOps
except ImportError:
    import Image
    import ImageOps


THUMBNAIL_SIZE = (75, 75)


def image_verify(f):
    try:
        Image.open(f).verify()
    except IOError:
        raise utils.NotAnImageException
