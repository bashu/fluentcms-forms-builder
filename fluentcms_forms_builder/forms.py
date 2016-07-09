# -*- coding: utf-8 -*-

from forms_builder.forms.forms import FormForForm

from .models import FieldEntry, FormEntry


class FormForForm(FormForForm):
    field_entry_model = FieldEntry

    class Meta:
        model = FormEntry
        exclude = ("form", "entry_time")
