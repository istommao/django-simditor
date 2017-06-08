"""demo admin."""
from django.contrib import admin

from app.models import News

from app.forms import SimditorForm


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """NewsAdmin."""

    form = SimditorForm
