from django.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel

from wagtail_site_inheritance.models import PageInheritanceMixin


class HomePage(PageInheritanceMixin, Page):
    pass


class OtherPage(PageInheritanceMixin, Page):
    intro = models.CharField(max_length=500)

    content_panels = Page.content_panels + [FieldPanel("intro")]
