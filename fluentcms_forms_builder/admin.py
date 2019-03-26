# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered

from forms_builder.forms.admin import (
    FieldAdmin as AbstractFieldAdmin, FormAdmin as AbstractFormAdmin)

from .models import Form, FormEntry, Field, FieldEntry


if 'forms_builder.forms' in settings.INSTALLED_APPS:
    from forms_builder.forms import models as forms

    try:
        admin.site.unregister(forms.Form)
    except NotRegistered:
        pass


class FieldAdmin(AbstractFieldAdmin):
    model = Field


class FormAdmin(AbstractFormAdmin):
    formentry_model = FormEntry
    fieldentry_model = FieldEntry
    inlines = (FieldAdmin,)
    view_on_site = False

    list_display = ("title", "email_copies", "total_entries", "admin_links")
    list_editable = ("email_copies", )

    fieldsets = [
        (None, {
            "fields": (
                "title", "intro", "button_text", "response", "redirect_url",
            ),
        })] + AbstractFormAdmin.fieldsets[1:]

admin.site.register(Form, FormAdmin)
