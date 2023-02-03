"""simditor widgets."""
from __future__ import absolute_import

import django
from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.serializers.json import DjangoJSONEncoder

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.functional import Promise

try:
    # Django >=2.1
    from django.forms.widgets import get_default_renderer
    IS_NEW_WIDGET = True
except ImportError:
    IS_NEW_WIDGET = False

try:
    # Django >=1.7
    from django.forms.utils import flatatt
except ImportError:
    # Django <1.7
    from django.forms.util import flatatt        # pylint disable=E0611, E0401

if django.VERSION >= (4, 0):
    from django.utils.encoding import force_str
else:
    from django.utils.encoding import force_text as force_str


class LazyEncoder(DjangoJSONEncoder):
    """LazyEncoder."""

    # pylint disable=E0202
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_str(obj)
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

        css_list = [
            'simditor/styles/simditor.min.css'
        ]

        if 'emoji' in settings.SIMDITOR_TOOLBAR:
            css_list.append('simditor/styles/simditor-emoji.css')

        if 'fullscreen' in settings.SIMDITOR_TOOLBAR:
            css_list.append('simditor/styles/simditor-fullscreen.min.css')

        if 'checklist' in settings.SIMDITOR_TOOLBAR:
            css_list.append('simditor/styles/simditor-checklist.min.css')

        if 'markdown' in settings.SIMDITOR_TOOLBAR:
            css_list.append('simditor/styles/simditor-markdown.min.css')

        css = {'all': tuple(settings.STATIC_URL + url for url in css_list)}

        jquery_list = ['simditor/scripts/jquery.min.js',
                       'simditor/scripts/module.min.js',
                       'simditor/scripts/hotkeys.min.js',
                       'simditor/scripts/uploader.min.js',
                       'simditor/scripts/simditor.min.js']

        if 'fullscreen' in settings.SIMDITOR_TOOLBAR:
            jquery_list.append('simditor/scripts/simditor-fullscreen.min.js')

        if 'checklist' in settings.SIMDITOR_TOOLBAR:
            jquery_list.append('simditor/scripts/simditor-checklist.min.js')

        if 'markdown' in settings.SIMDITOR_TOOLBAR:
            jquery_list.append('simditor/scripts/marked.min.js')
            jquery_list.append('simditor/scripts/to-markdown.min.js')
            jquery_list.append('simditor/scripts/simditor-markdown.min.js')

        if 'image' in settings.SIMDITOR_TOOLBAR:
            jquery_list.append('simditor/scripts/simditor-dropzone.min.js')

        if 'emoji' in settings.SIMDITOR_TOOLBAR:
            jquery_list.append('simditor/scripts/simditor-emoji.js')

        js = tuple(settings.STATIC_URL + url for url in jquery_list)

        try:

            js += (settings.STATIC_URL + 'simditor/simditor-init.js',)
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

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(self.attrs, attrs, name=name)

        params = ('simditor/widget.html', {
            'final_attrs': flatatt(final_attrs),
            'value': conditional_escape(force_str(value)),
            'id': final_attrs['id'],
            'config': JSON_ENCODE(self.config)
        })

        if renderer is None and IS_NEW_WIDGET:
            renderer = get_default_renderer()

        data = renderer.render(*params) if IS_NEW_WIDGET else render_to_string(*params)

        return mark_safe(data)
