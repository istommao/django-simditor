"""demo admin."""
from django.contrib import admin

from app.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """NewsAdmin."""
