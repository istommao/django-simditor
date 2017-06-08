"""demo."""
from django.db import models

from simditor.fields import RichTextField


class News(models.Model):
    """News."""
    content = RichTextField()
