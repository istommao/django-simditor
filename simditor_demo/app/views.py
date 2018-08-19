"""app views."""

from django import forms

from django.views import generic

from simditor.fields import RichTextFormField
try:
    from django.urls import reverse
except ImportError:  # Django < 2.0
    from django.core.urlresolvers import reverse


class SimditorForm(forms.Form):
    content = RichTextFormField()


class IndexView(generic.FormView):
    form_class = SimditorForm

    template_name = 'index.html'

    def get_success_url(self):
        return reverse('simditor-form')
