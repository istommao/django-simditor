"""simditor utils."""
from __future__ import absolute_import

import os.path
import random

import string

from django.core.files.storage import default_storage
from django.template.defaultfilters import slugify


class NotAnImageException(Exception):
    pass


def get_random_string():
    """Get random string."""
    return ''.join(random.sample(string.ascii_lowercase * 6, 6))


def get_slugified_name(filename):
    """get_slugified_name."""
    slugified = slugify(filename)
    return slugified or get_random_string()


def slugify_filename(filename):
    """ Slugify filename """
    name, ext = os.path.splitext(filename)
    slugified = get_slugified_name(name)
    return slugified + ext


def get_media_url(path):
    """
    Determine system file's media URL.
    """
    return default_storage.url(path)


def is_valid_image_extension(file_path):
    """is_valid_image_extension."""
    valid_extensions = ['.jpeg', '.jpg', '.gif', '.png']
    _, extension = os.path.splitext(file_path)
    return extension.lower() in valid_extensions
