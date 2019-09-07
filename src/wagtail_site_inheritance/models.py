from django.db import models

from wagtail.core.models import Page, Site
from wagtail_site_inheritance.wagtail_forms import SiteInheritanceAdminForm


class SiteInheritance(models.Model):
    site = models.OneToOneField(
        Site, related_name="inheritance_info", on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        Site, related_name="site_children", on_delete=models.PROTECT
    )

    base_form_class = SiteInheritanceAdminForm

    @property
    def root_page(self):
        return self.parent.root_page


class PageInheritanceItem(models.Model):
    page = models.ForeignKey(Page, related_name="+", on_delete=models.PROTECT)
    inherited_page = models.ForeignKey(Page, related_name="+", on_delete=models.CASCADE)

    #: Indicates wether the inherited page is modified in it's own tree, this means we
    #: don't want to sync all content anymore, only the readonly fields.
    modified = models.BooleanField(default=False)

    class Meta:
        unique_together = [("page", "inherited_page")]


class PageInheritanceMixin:
    def relative_url(self, current_site, request=None):
        """Always return a relative URL.

        We do this by providing the site of the page requested instead of the default
        implementation, this will always strip the domain from the URL.

        """
        return super().relative_url(current_site=self.get_site(), request=None)

    def get_admin_display_title(self):
        title = super().get_admin_display_title()
        item = PageInheritanceItem.objects.filter(inherited_page=self).first()
        if item and item.modified:
            return f"{title} - (Modified inherited)"
        elif item:
            return f"{title} (Inherited)"
        return title
