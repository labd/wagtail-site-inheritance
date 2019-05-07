from django.utils.translation import ugettext_lazy

from wagtail.admin.edit_handlers import ObjectList, TabbedInterface

from .forms import InheritedPageForm


def create_edit_handler(cls):
    tabs = []

    if cls.content_panels:
        tabs.append(ObjectList(cls.content_panels, heading=ugettext_lazy("Content")))
    if cls.promote_panels:
        tabs.append(ObjectList(cls.promote_panels, heading=ugettext_lazy("Promote")))
    if cls.settings_panels:
        tabs.append(
            ObjectList(
                cls.settings_panels,
                heading=ugettext_lazy("Settings"),
                classname="settings",
            )
        )

    edit_handler = InheritedTabbedInterface(tabs, base_form_class=InheritedPageForm)
    return edit_handler.bind_to(model=cls)


class InheritedTabbedInterface(TabbedInterface):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_form_bound(self):
        super().on_form_bound()

        # TODO: Removing this panels adds all field to main
        # if self.instance.inherit_from_page:
        #     del self.children[2]
        #     del self.children[1]
