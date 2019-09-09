from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class WagtailSiteInheritanceAppConfig(AppConfig):
    name = "wagtail_site_inheritance"
    verbose_name = _("Wagtail Site Inheritance")

    def ready(self):
        from wagtail_site_inheritance.receivers import register_handlers  # noqa

        register_handlers()
