from django.db import models
from wagtail import VERSION as wagtail_version

from wagtail_site_inheritance.models import PageInheritanceItem, PageInheritanceMixin

if wagtail_version >= (3, 0):
    from wagtail.models import Page
else:
    from wagtail.core.models import Page


class HomePage(PageInheritanceMixin, Page):
    body = models.CharField(max_length=500, default="")
    custom_content = models.CharField(max_length=500, default="")
    inherit_readonly_fields = ["body"]

    def full_clean(self, *args, **kwargs):
        """Apply fixups that need to happen before per-field validation occurs.

        Overridden to ensure translation keys remain consistent with inherited pages.
        If there's a mismatch, we ensure this is logged and automatically correct it.
        """
        is_new = self.pk is None
        if not is_new:
            try:
                item = PageInheritanceItem.objects.get(inherited_page=self)
                if (
                    not self.translation_key  # type: ignore
                    == item.inherited_page.translation_key
                ):
                    self.translation_key = item.inherited_page.translation_key
                if not self.locale_id == item.inherited_page.locale_id:
                    self.locale = item.inherited_page.locale
            except PageInheritanceItem.DoesNotExist:
                # All good. No inheritance item exists (yet), so we don't have to
                # check if the translation key is correct.
                pass

        super().full_clean(*args, **kwargs)

