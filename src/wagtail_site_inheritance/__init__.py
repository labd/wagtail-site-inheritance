from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

__version__ = "1.0.0"


class WagtailSiteInheritanceAppConfig(AppConfig):
    name = "wagtail_site_inheritance"
    verbose_name = _("Wagtail Site Inheritance")

    def ready(self):
        from wagtail_site_inheritance.receivers import register_handlers  # noqa

        register_handlers()
