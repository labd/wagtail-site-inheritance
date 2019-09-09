from django.db.models import OneToOneField
from django.utils.translation import ugettext_lazy as _
from modelcluster.models import get_all_child_m2m_relations, get_all_child_relations
from wagtail.core import hooks
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from wagtail_site_inheritance import models, permissions, views


class SiteInheritanceAdmin(ModelAdmin):
    model = models.SiteInheritance
    menu_icon = "link"
    menu_label = _("Site Inheritance")
    menu_order = 10000
    list_filter = ["parent"]
    list_display = ["site", "parent"]
    add_to_settings_menu = True
    delete_view_class = views.SiteInheritanceDeleteView
    permission_helper_class = permissions.SiteInheritancePermissionHelper


modeladmin_register(SiteInheritanceAdmin)


# FIXME: This is a working example of the copy / sync methods, it needs refactoring
@hooks.register("after_edit_page")
@hooks.register("after_create_page")
def update_or_create_copies(request, page):
    """
    Copy the pages to all inherited sites.

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

    create_non_existing_pages(request, page, parent_page)
    sync_existing_pages(request, page)

    # Mark edited page as modified
    models.PageInheritanceItem.objects.filter(
        inherited_page=page, modified=False
    ).update(modified=True)


def create_non_existing_pages(request, page, parent_page):
    # Create non existing pages in other trees.
    inherited_parents = [
        pii.inherited_page.get_parent()
        for pii in models.PageInheritanceItem.objects.filter(page=page)
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


def sync_existing_pages(request, page):
    """
    Update existing pages (sync all required content).
    """
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
        customizable_fields = getattr(page, "customizable_fields", [])
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

        # copy child m2m relations
        for related_field in get_all_child_m2m_relations(page):
            field = getattr(page, related_field.name)
            if field and hasattr(field, 'all'):
                values = field.all()
                if values:
                    values[related_field.name] = values

        for inheritance_item in items:
            # always get the specific class instance, or the revision will only contain the Page attributes
            copy_page = inheritance_item.inherited_page.specific

            for field_name, value in values.items():
                if inheritance_item.modified and field_name in customizable_fields:
                    continue
                setattr(copy_page, field_name, value)

            # Copy child objects
            for child_relation in get_all_child_relations(page):
                accessor_name = child_relation.get_accessor_name()

                parental_key_name = child_relation.field.attname
                child_objects = getattr(page, accessor_name, None)

                if child_objects:
                    for child_object in child_objects.all():
                        child_object.pk = None
                        setattr(child_object, parental_key_name, copy_page.id)
                        child_object.save()

            copy_page.save()
            revision = copy_page.save_revision(
                user=request.user,
                submitted_for_moderation=bool(request.POST.get("action-submit")),
            )
            revision.publish()
