"""simditor fields."""
from django import forms
from django.db import models

from .widgets import SimditorWidget


class RichTextFormField(forms.fields.CharField):
    """RichTextFormField."""

    def __init__(self, config_name='default', *args, **kwargs):
        kwargs.update(
            {
                'widget': SimditorWidget(
                    config_name=config_name
                )
            }
        )
        super(RichTextFormField, self).__init__(*args, **kwargs)


class RichTextField(models.TextField):
    """RichTextField."""

    def __init__(self, *args, **kwargs):
        self.config_name = kwargs.pop('config_name', 'default')
        super(RichTextField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self._get_form_class(),
            'config_name': self.config_name
        }
        defaults.update(kwargs)
        return super(RichTextField, self).formfield(**defaults)

    @staticmethod
    def _get_form_class():
        return RichTextFormField
