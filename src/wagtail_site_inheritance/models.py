from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail import VERSION as wagtail_version
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.admin.forms import WagtailAdminPageForm

from wagtail_site_inheritance.forms import get_readonly_widget
from wagtail_site_inheritance.wagtail_forms import SiteInheritanceAdminForm

if wagtail_version >= (3, 0):
    from wagtail.models import Page, Site
else:
    from wagtail.core.models import Page, Site


class SiteInheritance(models.Model):
    parent = models.ForeignKey(
        Site,
        verbose_name=_("parent site"),
        related_name="site_children",
        on_delete=models.PROTECT,
        help_text=_("Choose the site to inherit from."),
    )
    site = models.OneToOneField(
        Site,
        verbose_name=_("child site"),
        related_name="inheritance_info",
        on_delete=models.CASCADE,
    )

    base_form_class = SiteInheritanceAdminForm
    panels = [MultiFieldPanel(children=[FieldPanel("parent"), FieldPanel("site")])]

    def __str__(self):
        return _("SiteInheritance from %(parent_site)s to %(child_site)s") % {
            "parent_site": self.parent,
            "child_site": self.site,
        }


class PageInheritanceItem(models.Model):
    page = models.ForeignKey(Page, related_name="+", on_delete=models.PROTECT)
    inherited_page = models.ForeignKey(Page, related_name="+", on_delete=models.CASCADE)

    #: Indicates whether the inherited page is modified in it's own tree, this means we
    #: don't want to sync all content anymore, only the readonly fields.
    modified = models.BooleanField(default=False)

    class Meta:
        unique_together = [("page", "inherited_page")]

    def __str__(self):
        return _(
            "Page: %(title)s, inherited from: %(inherited_title)s, modified: %(modified)s"
        ) % {
            "title": self.page.title,
            "inherited_title": self.inherited_page.title,
            "modified": self.modified,
        }


class PageInheritanceForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        is_inherited = PageInheritanceItem.objects.filter(
            inherited_page=self.instance
        ).exists()
        if not is_inherited:
            return

        # Make fields readonly if page is inherited
        for field_name, field in self.fields.items():
            if field_name in self.instance.inherit_readonly_fields:
                # Make some fields readonly
                self.fields[field_name].widget = get_readonly_widget(
                    self.fields[field_name]
                )


class PageInheritanceMixin:
    def relative_url(self, current_site, request=None):
        """
        Always return a relative URL.

        We do this by providing the site of the page requested instead of the default
        implementation, this will always strip the domain from the URL.
        """
        url_parts = self.get_url_parts(request=request)
        site_id, root_url, page_path = url_parts
        return page_path

    def get_admin_display_title(self):
        title = super().get_admin_display_title()
        item = PageInheritanceItem.objects.filter(inherited_page=self).first()
        if item and item.modified:
            return _("%(title)s - (inherited + modified)") % {"title": title}
        elif item:
            return _("%(title)s - (inherited)") % {"title": title}
        return title

    base_form_class = PageInheritanceForm

    # fields that should be readonly on inherited pages
    inherit_readonly_fields = []

    # field that shouldn't be updated during copy
    exclude_fields_in_copy = []
