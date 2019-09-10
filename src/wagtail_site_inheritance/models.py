from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.core.models import Page, Site

from wagtail_site_inheritance.wagtail_forms import SiteInheritanceAdminForm


class SiteInheritance(models.Model):
    parent = models.ForeignKey(
        Site, related_name="site_children", on_delete=models.PROTECT
    )
    site = models.OneToOneField(
        Site, related_name="inheritance_info", on_delete=models.CASCADE
    )

    base_form_class = SiteInheritanceAdminForm
    panels = [MultiFieldPanel(children=[FieldPanel("parent"), FieldPanel("site")])]

    def __str__(self):
        parent_site = self.parent.site_name or self.parent.hostname
        child_site = self.site.site_name or self.site.hostname
        return f"SiteInheritance from {parent_site} to {child_site}"


class PageInheritanceItem(models.Model):
    page = models.ForeignKey(Page, related_name="+", on_delete=models.PROTECT)
    inherited_page = models.ForeignKey(Page, related_name="+", on_delete=models.CASCADE)

    #: Indicates whether the inherited page is modified in it's own tree, this means we
    #: don't want to sync all content anymore, only the readonly fields.
    modified = models.BooleanField(default=False)

    class Meta:
        unique_together = [("page", "inherited_page")]

    def __str__(self):
        return f"Page: {self.page.title} Inherited page: {self.inherited_page.title} Modified: {self.modified}"


class PageInheritanceForm(WagtailAdminPageForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # assumes the default site is the site to inherit from,
        # the alternative is querying SiteInheritance.
        site = self.instance.get_site()
        if not site or (site and site.is_default_site):
            return

        for field in self.instance.editable_inherited_fields:
            if field in self.fields:
                # FIXME: this doesn't work for streamfields...
                self.fields[field].disabled = True


class PageInheritanceMixin:
    def relative_url(self, current_site, request=None):
        """
        Always return a relative URL.

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

    base_form_class = PageInheritanceForm

    # fields that can be edited in inherited pages
    editable_inherited_fields = []
