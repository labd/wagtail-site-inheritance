from django import forms
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.forms import WagtailAdminModelForm


class SiteInheritanceAdminForm(WagtailAdminModelForm):
    class Meta:
        fields = ["site", "parent"]

    def clean_parent(self):
        """Validate the site and parent site root pages.

        A valid SiteTree can only be created if the root pages specific page type are the
        same, otherwise we will get errors when we try to copy the pages.

        """
        site = self.cleaned_data.get("site", False)
        parent = self.cleaned_data.get("parent", False)
        if not isinstance(site.root_page.specific, parent.root_page.specific_class):
            raise forms.ValidationError(
                _("Both sites should have the same root_page type")
            )
        return parent

    def save(self, **kwargs):
        """Save the SiteTree and make sure the homepages get linked.

        Since the homepages already exist, we need to mark them as modified, otherwise
        all existing content will be lost.

        """
        instance = super().save(**kwargs)
        from wagtail_site_inheritance.models import PageInheritanceItem  # cyclic import

        PageInheritanceItem.objects.create(
            page=self.cleaned_data["parent"].root_page,
            inherited_page=self.cleaned_data["site"].root_page,
            modified=True,
        )

        return instance