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


class LazyEncoder(DjangoJSONEncoder):
    """LazyEncoder."""

    # pylint disable=E0202
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)

JSON_ENCODE = LazyEncoder().encode

DEFAULT_TOOLBAR = [
    'title', 'bold', 'italic', 'underline', 'strikethrough', 'fontScale',
    'color', '|', 'ol', 'ul', 'blockquote', 'code', 'table', '|', 'link',
    'image', 'hr', '|', 'indent', 'outdent', 'alignment', 'checklist',
    'markdown', 'fullscreen'
]

DEFAULT_CONFIG = {
    'toolbar': DEFAULT_TOOLBAR,
    'cleanPaste': True,
    'tabIndent': True,
    'pasteImage': True,
    'textarea': '#editor',
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
            js += (jquery_url, )
        try:
            js += (
                settings.STATIC_URL + 'simditor/scripts/simditor.main.min.js',
                settings.STATIC_URL + 'simditor/simditor-init.js',
            )
        except AttributeError:
            raise ImproperlyConfigured("django-simditor requires \
                     SIMDITOR_MEDIA_PREFIX setting. This setting specifies a \
                    URL prefix to the ckeditor JS and CSS media (not \
                    uploaded media). Make sure to use a trailing slash: \
                    SIMDITOR_MEDIA_PREFIX = '/media/simditor/'")

    def __init__(self, config_name='default', extra_plugins=None,
                 external_plugin_resources=None, *args, **kwargs):
        super(SimditorWidget, self).__init__(*args, **kwargs)
        # Setup config from defaults.
        self.config = DEFAULT_CONFIG.copy()

        # Try to get valid config from settings.
        configs = getattr(settings, 'SIMDITOR_CONFIGS', None)
        if configs:
            if isinstance(configs, dict):
                # Make sure the config_name exists.
                if config_name in configs:
                    config = configs[config_name]
                    # Make sure the configuration is a dictionary.
                    if not isinstance(config, dict):
                        raise ImproperlyConfigured(
                            'CKEDITOR_CONFIGS["%s"] setting must be a '
                            'dictionary type.' % config_name
                        )
                    # Override defaults with settings config.
                    self.config.update(config)
                else:
                    raise ImproperlyConfigured("No configuration named '%s' \
                            found in your CKEDITOR_CONFIGS setting." %
                                               config_name)
            else:
                raise ImproperlyConfigured(
                    'CKEDITOR_CONFIGS setting must be a dictionary type.')

        extra_plugins = extra_plugins or []

        if extra_plugins:
            self.config['extraPlugins'] = ','.join(extra_plugins)

        self.external_plugin_resources = external_plugin_resources or []

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

        external_plugin_resources = [[force_text(a), force_text(b), force_text(c)]
                                     for a, b, c in self.external_plugin_resources]

        return mark_safe(render_to_string('simditor/widget.html', {
            'value': conditional_escape(force_text(value)),
            'id': final_attrs['id'],
            'config': JSON_ENCODE(self.config),
            'external_plugin_resources': JSON_ENCODE(external_plugin_resources)
        }))
