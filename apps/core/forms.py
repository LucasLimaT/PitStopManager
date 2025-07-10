from django import forms


class BaseBootstrapForm(forms.ModelForm):
    WIDGET_ATTRS = {
        "select": {"class": "form-select"},
        "text": {"class": "form-control"},
        "datetime": {"class": "form-control", "type": "datetime-local"},
        "textarea": {"class": "form-control"},
        "email": {"class": "form-control"},
        "number": {"class": "form-control"},
        "password": {"class": "form-control"},
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap_classes()

    def apply_bootstrap_classes(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update(self.WIDGET_ATTRS["select"])
            elif isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update(self.WIDGET_ATTRS["text"])
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs.update(self.WIDGET_ATTRS["datetime"])
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update(self.WIDGET_ATTRS["textarea"])
            elif isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update(self.WIDGET_ATTRS["email"])
            elif isinstance(field.widget, forms.NumberInput):
                field.widget.attrs.update(self.WIDGET_ATTRS["number"])
            elif isinstance(field.widget, forms.PasswordInput):
                field.widget.attrs.update(self.WIDGET_ATTRS["password"])
