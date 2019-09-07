from django.db.models import OneToOneField
from django.utils.translation import ugettext_lazy as _
from wagtail.core import hooks
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from wagtail_site_inheritance import models


class SiteInheritanceAdmin(ModelAdmin):
    model = models.SiteInheritance
    menu_icon = "link"
    menu_label = _("Site Inheritance")
    menu_order = 10000
    list_filter = ["parent"]
    list_display = ["parent", "site"]
    add_to_settings_menu = True


modeladmin_register(SiteInheritanceAdmin)


# FIXME: This is a working example of the copy / sync methods, it needs refactoring
@hooks.register("after_edit_page")
@hooks.register("after_create_page")
def update_or_create_copies(request, page):
    """Copy the pages to all inherited sites.

    We only copy the pages when they're published as well, this way the other sites won't
    be able to see content which is still a draft.

    """
    parent_page = page.get_parent()
    parent_page_perms = parent_page.permissions_for_user(request.user)

    is_publishing = (
        bool(request.POST.get("action-publish"))
        and parent_page_perms.can_publish_subpage()
    )
    if not is_publishing:
        return

    # Create non existing pages in other trees.
    inherited_parents = [
        o.inherited_page.get_parent()
        for o in models.PageInheritanceItem.objects.filter(page=page)
    ]
    for inheritance_item in models.PageInheritanceItem.objects.filter(page=parent_page):
        if inheritance_item.inherited_page in inherited_parents:
            continue

        page_copy = page.copy(
            to=inheritance_item.inherited_page,
            copy_revisions=False,
            keep_live=False,  # We do this so we won't get a new draft revision
            user=request.user,
            update_attrs={"live": True, "has_unpublished_changes": False},
        )

        models.PageInheritanceItem.objects.create(page=page, inherited_page=page_copy)

    # Update existing pages (sync all required content)
    skip_fields = [
        "id",
        "path",
        "depth",
        "numchild",
        "url_path",
        "path",
        "index_entries",
        "live_revision",
        "content_type",
    ]

    items = models.PageInheritanceItem.objects.filter(page=page)
    if items.exists():
        values = {}
        for field in page._meta.get_fields():
            # FIXME: Instead of stepping over difficult fields we should copy their
            # contents too, the wagtail.core.Page.copy() method has some examples on how
            # to do that.
            if (
                field.name in skip_fields
                or field.auto_created
                or field.many_to_many
                or (isinstance(field, OneToOneField) and field.remote_field.parent_link)
            ):
                continue

            values[field.name] = getattr(page, field.name)

        for inheritance_item in items:
            # FIXME: Update readonly fields instead of stepping over the complete page.
            if not inheritance_item.modified:
                continue

            copy_page = inheritance_item.inherited_page
            for field_name, value in values.items():
                setattr(copy_page, field_name, value)

            copy_page.save()
            revision = copy_page.save_revision(
                user=request.user,
                submitted_for_moderation=bool(request.POST.get("action-submit")),
            )
            revision.publish()

    # Mark edited page as modified
    item = models.PageInheritanceItem.objects.filter(
        inherited_page=page, modified=True
    ).first()
    if item:
        item.modified = False
        item.save(update_fields=["modified"])
