"""simditor widgets."""
from __future__ import absolute_import

from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.serializers.json import DjangoJSONEncoder

from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.functional import Promise

try:
    # Django >=1.7
    from django.forms.utils import flatatt
except ImportError:
    # Django <1.7
    from django.forms.util import flatatt        # pylint disable=E0611, E0401


class LazyEncoder(DjangoJSONEncoder):
    """LazyEncoder."""

    # pylint disable=E0202
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)

JSON_ENCODE = LazyEncoder().encode


FULL_TOOLBAR = [
    'title', 'bold', 'italic', 'underline', 'strikethrough', 'fontScale',
    'color', '|', 'ol', 'ul', 'blockquote', 'code', 'table', '|', 'link',
    'image', 'hr', '|', 'indent', 'outdent', 'alignment', 'checklist',
    'markdown', 'fullscreen'
]

DEFAULT_TOOLBAR = [
    'title', 'bold', 'italic', 'underline', 'strikethrough', 'fontScale',
    'color', '|', 'ol', 'ul', 'blockquote', 'table', '|', 'link',
    'image', 'hr', '|', 'indent', 'outdent', 'alignment'
]

DEFAULT_CONFIG = {
    'toolbar': DEFAULT_TOOLBAR,
    'cleanPaste': True,
    'tabIndent': True,
    'pasteImage': True,
    'upload': {
        'url': '/',
        'fileKey': 'file'
    }
}


class SimditorWidget(forms.Textarea):
    """
    Widget providing Simditor for Rich Text Editing.abs
    Supports direct image uploads and embed.
    """
    class Media:
        """Media."""
        css = {
            'all': (
                settings.STATIC_URL + 'simditor/styles/simditor.main.min.css',
            )
        }

        js = ()
        jquery_url = getattr(settings, 'SIMDITOR_JQUERY_URL', None)
        if jquery_url:
            js += (jquery_url,)
        try:
            js += (
                settings.STATIC_URL + 'simditor/scripts/simditor.main.min.js',
                settings.STATIC_URL + 'simditor/scripts/marked.min.js',
                settings.STATIC_URL + 'simditor/scripts/simditor.ext.min.js',
                settings.STATIC_URL + 'simditor/simditor-init.js'
            )
        except AttributeError:
            raise ImproperlyConfigured("django-simditor requires \
                     SIMDITOR_MEDIA_PREFIX setting. This setting specifies a \
                    URL prefix to the ckeditor JS and CSS media (not \
                    uploaded media). Make sure to use a trailing slash: \
                    SIMDITOR_MEDIA_PREFIX = '/media/simditor/'")

    def __init__(self, *args, **kwargs):
        super(SimditorWidget, self).__init__(*args, **kwargs)
        # Setup config from defaults.
        self.config = DEFAULT_CONFIG.copy()

        # Try to get valid config from settings.
        configs = getattr(settings, 'SIMDITOR_CONFIGS', None)
        if configs:
            if isinstance(configs, dict):
                self.config.update(configs)
            else:
                raise ImproperlyConfigured(
                    'SIMDITOR_CONFIGS setting must be a dictionary type.')

    def build_attrs(self, base_attrs, extra_attrs=None, **kwargs):
        """
        Helper function for building an attribute dictionary.
        This is combination of the same method from Django<=1.10 and Django1.11
        """
        attrs = dict(base_attrs, **kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)
        return attrs

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(self.attrs, attrs, name=name)

        return mark_safe(render_to_string('simditor/widget.html', {
            'final_attrs': flatatt(final_attrs),
            'value': conditional_escape(force_text(value)),
            'id': final_attrs['id'],
            'config': JSON_ENCODE(self.config)
        }))
