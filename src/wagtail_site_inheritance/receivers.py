from django.db import transaction
from wagtail.core.signals import page_unpublished

from wagtail_site_inheritance.models import PageInheritanceItem


def remove_copies(sender, instance, **kwargs):
    """
    Remove all published copies when unpublishing a page.

    For now we remove all non modified copies of the inherited page on unpublish for the
    modified copies we only remove the page link and make them "stand-alone".
    """
    items = PageInheritanceItem.objects.filter(page=instance)
    if not items.exists():
        return

    with transaction.atomic():
        for item in items:
            if not item.modified:
                item.inherited_page.delete()

            item.delete()


def register_handlers():
    page_unpublished.connect(remove_copies)
