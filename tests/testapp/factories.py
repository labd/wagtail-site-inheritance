import factory
from wagtail_factories import CharBlockFactory, PageFactory

from tests.testapp.models import HomePage


class HomePageFactory(PageFactory):
    body = factory.SubFactory(CharBlockFactory, value="Body Text")
    custom_content = factory.SubFactory(CharBlockFactory, value="Custom content text")

    class Meta:
        model = HomePage
