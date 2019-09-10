from django.db import models
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from wagtail_site_inheritance.models import PageInheritanceMixin


class HomePage(PageInheritanceMixin, Page):
    pass


class OtherPage(PageInheritanceMixin, Page):
    intro = models.CharField(max_length=500)
    custom_content = models.CharField(max_length=500, default="")
    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="full title")),
            ("paragraph", blocks.RichTextBlock()),
        ]
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("custom_content"),
        StreamFieldPanel("body"),
    ]

    editable_inherited_fields = ["custom_content"]
