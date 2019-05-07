from django import forms
from django.utils.translation import ugettext as _

from wagtail.admin.forms.pages import WagtailAdminPageForm


class InheritedPageForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.inherit_from_page:
            inherit_readonly_fields = getattr(
                self.instance, "inherit_readonly_fields", []
            )
            for field in inherit_readonly_fields:
                self.fields[field].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        # if 'slug' in self.cleaned_data:
        #     self.add_error('slug', forms.ValidationError(_("This slug is already in use")))
        return cleaned_data
