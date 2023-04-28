from django.db import transaction
from wagtail import VERSION as wagtail_version
from wagtail.contrib.modeladmin.views import DeleteView

from wagtail_site_inheritance.models import PageInheritanceItem

if wagtail_version >= (3, 0):
    from wagtail.models import Page
else:
    from wagtail.core.models import Page


class SiteInheritanceDeleteView(DeleteView):
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        """
        Remove the PageInheritanceItems before removing the SiteInheritance.

        This way we ensure that the site will be detached from further syncing and
        prevent a lot of unexpected behavior.
        """
        pages_in_site = Page.objects.in_site(self.instance.site).values("pk")
        PageInheritanceItem.objects.filter(inherited_page_id__in=pages_in_site).delete()
        return super().post(request, *args, **kwargs)
