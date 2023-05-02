from tests.fixtures import *
from tests.testapp.models import HomePage
from wagtail_site_inheritance.wagtail_hooks import update_or_create_copies


@pytest.mark.django_db
def test_update_or_create_copies(site_setup, rf):
    form_data = {"action-publish": "action-publish"}
    req = rf.post(
        path=f"/cms/pages/{site_setup.main_site.root_page.id}/edit/", data=form_data
    )
    req.user.is_active = True
    req.user.is_superuser = True
    req.user.save()
    update_or_create_copies(req, site_setup.main_site.root_page)

    main_page = HomePage.objects.get(id=site_setup.main_site.root_page.id)
    inheriting_page = HomePage.objects.get(id=site_setup.inheriting_site.root_page.id)

    # body is inherited, inheriting site should have inherited the value of the main site
    assert main_page.body == "Main site body"
    assert inheriting_page.body == "Main site body"

    # custom content is not inherited, main site value should be different
    assert main_page.custom_content == "Main site custom content"
    assert inheriting_page.custom_content == "Custom content text"