from django.db import models
from django.http import Http404
from django.utils.functional import cached_property

from wagtail.core.models import Page

from .edit_handler import create_edit_handler


class SiteTree(models.Model):
    site = models.OneToOneField(
        "wagtailcore.Site", related_name="inheritance_info", on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        "wagtailcore.Site", related_name="site_children", on_delete=models.PROTECT
    )

    @property
    def root_page(self):
        return self.parent.root_page


class SiteInheritanceItem(models.Model):
    page = models.ForeignKey(
        "wagtailcore.Page",
        related_name="+",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    inherited_page = models.ForeignKey(
        "wagtailcore.Page",
        related_name="+",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = [("page", "inherited_page")]


class PageInheritanceMixin:
    @cached_property
    def is_inherited(self):
        return getattr(self, "_is_inherited", False)  # Set via annotation

    @cached_property
    def inherit_from_page(self):
        item = SiteInheritanceItem.objects.filter(inherited_page=self).first()
        if item:
            return item.page

    @property
    def is_navigable(self):
        if self.is_inherited:
            return False
        return super().is_navigable

    def route(self, request, path_components):
        try:
            return super().route(request, path_components)
        except Http404:
            site = self.get_site()
            parent_site = site.inheritance_info.parent
            return parent_site.root_page.route(request, path_components)

    def get_admin_display_title(self):
        name = super().get_admin_display_title()
        if self.inherit_from_page:
            return f"{name} - (Modified inherited)"
        if self.is_inherited:
            return f"{name} (Inherited)"
        return name

    @classmethod
    def _slug_is_available(cls, slug, parent_page, instance):
        return False
