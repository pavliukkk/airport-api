from rest_framework.relations import RelatedField
from rest_framework.renderers import BrowsableAPIRenderer


class CustomBrowsableAPIRenderer(BrowsableAPIRenderer):
    def render_form_for_serializer(self, serializer):
        airport_choices = None

        for field in serializer.fields.values():
            if isinstance(field, RelatedField) and field.field_name in (
                "source",
                "destination",
            ):
                if airport_choices is None:
                    airport_choices = field.get_choices()

                field.get_choices = lambda cutoff=None, choices=airport_choices: (
                    dict(list(choices.items())[:cutoff]) if cutoff else choices
                )

        return super().render_form_for_serializer(serializer)
