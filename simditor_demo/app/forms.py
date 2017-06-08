"""app forms."""
from __future__ import absolute_import

from django import forms

from simditor.fields import RichTextFormField


class SimditorForm(forms.ModelForm):
    """SimditorForm."""
    content = RichTextFormField()
