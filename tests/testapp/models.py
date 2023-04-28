from django.db import models
from wagtail import VERSION as wagtail_version

from wagtail_site_inheritance.models import PageInheritanceMixin

if wagtail_version >= (3, 0):
    from wagtail.models import Page
else:
    from wagtail.core.models import Page


class HomePage(PageInheritanceMixin, Page):
    body = models.CharField(max_length=500, default="")
    custom_content = models.CharField(max_length=500, default="")
    inherit_readonly_fields = ["body"]
