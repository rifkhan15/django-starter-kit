import django_filters

class BaseFilterSet(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.form.fields.values():

            # Auto submit on change
            field.widget.attrs["onchange"] = "this.form.submit();"

            # Replace empty label "-----" with "All"
            if hasattr(field, "empty_label"):
                field.empty_label = "All"

            # Also fix widget-level empty option (FK dropdowns)
            if hasattr(field.widget, "choices"):
                choices = list(field.widget.choices)

                if choices and choices[0][0] == "":
                    choices[0] = ("", "All")
                    field.widget.choices = choices

