from django.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel

from wagtail_site_inheritance.models import PageInheritanceMixin


class HomePage(PageInheritanceMixin, Page):
    pass


class OtherPage(PageInheritanceMixin, Page):
    intro = models.CharField(max_length=500)
    custom_content = models.CharField(max_length=500, default="")

    content_panels = Page.content_panels + [FieldPanel("intro"), FieldPanel("custom_content")]

    @property
    def customizable_fields(self):
        """
        Fields that can be overwritten in other sites.
        """
        return ["custom_content"]
