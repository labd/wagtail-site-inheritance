from django.conf import settings
from django.conf.urls import url
from django.db.models import BooleanField, Case, CharField, F, Value, When
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from wagtail.admin import widgets as wagtailadmin_widgets
from wagtail.admin.menu import MenuItem
from wagtail.core import hooks
from wagtail.core.models import Site
from wagtail.users.widgets import UserListingButton
from wagtail_site_inheritance import models, views


@hooks.register("register_admin_urls")
def urlpatterns():
    return [
        url(
            r"^site-inheritance/$",
            views.SiteInheritanceListView.as_view(),
            name="wagtail_site_inheritance",
        ),
        url(
            r"^site-inheritance/create$",
            views.SiteInheritanceCreateView.as_view(),
            name="wagtail_site_inheritance_create",
        ),
        url(
            r"^site-inheritance/clone-inherited-page/(?P<parent_pk>\d+)/(?P<pk>\d+)$",
            views.PageCloneInheritedView.as_view(),
            name="wagtail_site_inheritance_clone_inherited_page",
        ),
    ]


@hooks.register("register_settings_menu_item")
def register_menu_item():
    return MenuItem(
        "Site Inheritance",
        reverse("wagtail_site_inheritance"),
        classnames="icon icon-link",
        order=10000,
    )


@hooks.register("construct_explorer_page_queryset")
def alter_page_explorer(parent_page, pages, request):
    site = parent_page.get_site()
    if not site:
        return pages

    try:
        inherited_root = site.inheritance_info.root_page
    except Site.inheritance_info.RelatedObjectDoesNotExist:
        return pages

    if inherited_root is None:
        return pages

    # TODO: get correct children
    path = parent_page.relative_url(site)
    inherited_pages = inherited_root.get_children().exclude(
        pk__in=models.SiteInheritanceItem.objects.filter(
            inherited_page__in=pages
        ).values("page")
    )

    all_pages = pages | inherited_pages

    all_pages = all_pages.annotate(
        _is_inherited=Case(
            When(path__startswith=parent_page.path, then=Value(0)),
            default=Value(1),
            output_field=BooleanField(),
        )
    )
    return all_pages


@hooks.register("construct_page_listing_buttons")
def page_listing_buttons(buttons, page, page_perms, is_parent=False, context=None):
    if getattr(page, 'is_inherited', False):
        buttons.clear()
        parent_page = context.get("parent_page")

        if parent_page:
            buttons.append(
                wagtailadmin_widgets.Button(
                    "Edit",
                    reverse(
                        "wagtail_site_inheritance_clone_inherited_page",
                        args=[parent_page.id, page.id],
                    ),
                    priority=10,
                )
            )
