from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

__all__ = ["get_readonly_widget"]


def get_readonly_widget(field):
    widget = field.widget
    widget_class = widget.__class__

    if field.label:
        text_display = (
            _("The value of %s is inherited from the parent site.")
            % str(field.label).lower()
        )
    else:
        text_display = _("The value of this field is inherited from the parent site.")

    # Add ReadOnlyMixin to this widget instance
    namespaces = {"text_display": text_display}
    widget.__class__ = type("ReadonlyWidget", (ReadonlyMixin, widget_class), namespaces)

    return field.widget


class ReadonlyMixin:
    def render(self, *args, **kwargs):
        original_content = super().render(*args, **kwargs)

        # TODO, move css to separate file
        return mark_safe(
            """
            <style type="text/css">
                .readonly_widget .input:before { display: none; }
                .readonly_widget .field-content .readonly-label { padding: 1.5em 0; }
                .object.stream-field .field-content .readonly-label,
                .object.full .field-content .readonly-label { padding-left: 50px; padding-right: 50px; }
            </style>
            <div class="readonly-hidden" hidden>%s</div>
            <div class="readonly-label">%s</div>
        """
            % (original_content, self.text_display)
        )
