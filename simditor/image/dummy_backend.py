"""simditor image pillow_backend."""
from __future__ import absolute_import

from simditor import utils


def image_verify(file_object):
    """image_verify."""
    if not utils.is_valid_image_extension(file_object.name):
        raise utils.NotAnImageException
