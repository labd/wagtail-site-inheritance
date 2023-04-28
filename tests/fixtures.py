from dataclasses import dataclass

import factory
import pytest
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.backends.db import SessionStore
from django.test.client import RequestFactory as BaseRequestFactory
from wagtail import VERSION as wagtail_version
from wagtail_factories import PageFactory, SiteFactory

from tests.testapp.factories import HomePageFactory
from wagtail_site_inheritance.models import PageInheritanceItem, SiteInheritance

if wagtail_version >= (3, 0):
    from wagtail.models import Site
else:
    from wagtail.core.models import Site


@dataclass
class SiteSetup:
    main_site: Site
    inheriting_site: Site


@pytest.fixture
def site_setup() -> SiteSetup:
    root_page = PageFactory(title="Root")
    main_site = SiteFactory(
        root_page=factory.SubFactory(
            HomePageFactory,
            parent=root_page,
            slug="main-site",
            title="Main site root page",
            body__value="Main site body",
            custom_content__value="Main site custom content",
        ),
        site_name="Main Site",
    )
    inheriting_site = SiteFactory(
        root_page=factory.SubFactory(
            HomePageFactory,
            parent=root_page,
            slug="inheriting-site",
            title="Inheriting site root page",
        ),
        site_name="Inheriting site",
    )

    SiteInheritance(parent=main_site, site=inheriting_site).save()
    PageInheritanceItem(
        page=main_site.root_page, inherited_page=inheriting_site.root_page
    ).save()

    return SiteSetup(main_site=main_site, inheriting_site=inheriting_site)


@pytest.fixture()
def rf():
    """Return a RequestFactory instance."""
    return RequestFactory()


class RequestFactory(BaseRequestFactory):
    def request(self, user=None, **request):
        request = super(RequestFactory, self).request(**request)
        request.user = User()
        request.session = SessionStore()
        request._messages = FallbackStorage(request)

        return request
