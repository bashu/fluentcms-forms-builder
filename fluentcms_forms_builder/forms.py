from forms_builder.forms.forms import FormForForm as AbstractFormForForm

from .models import FieldEntry, FormEntry


class FormForForm(AbstractFormForForm):
    field_entry_model = FieldEntry

    class Meta:
        model = FormEntry
        exclude = ("form", "entry_time")
