# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext, ugettext_lazy as _

from fluent_contents.models.db import ContentItem
from forms_builder.forms.models import (
    AbstractFormEntry, AbstractFieldEntry, AbstractField, AbstractForm)
from any_urlfield.models import AnyUrlField

from .meta import AbstractClassWithoutFieldsNamed as without


class FormEntry(AbstractFormEntry):
    form = models.ForeignKey("Form", related_name="entries")


class FieldEntry(AbstractFieldEntry):
    entry = models.ForeignKey("FormEntry", related_name="fields")


class Form(without(AbstractForm, 'redirect_url')):

    redirect_url = AnyUrlField(
        _("Redirect url"),
        max_length=200,
        blank=True, null=True,
        help_text=_("An alternate URL to redirect to after form submission"),
    )

    def get_absolute_url(self):
        raise NotImplementedError

    def admin_links(self):
        kw = {"args": (self.id,)}
        links = [
            (_("Filter entries"), reverse("admin:form_entries", **kw)),
            (_("View all entries"), reverse("admin:form_entries_show", **kw)),
            (_("Export all entries"), reverse("admin:form_entries_export", **kw)),
        ]
        for i, (text, url) in enumerate(links):
            links[i] = "<a href='%s'>%s</a>" % (url, ugettext(text))
        return "<br>".join(links)
    admin_links.allow_tags = True
    admin_links.short_description = ""


class Field(AbstractField):

    form = models.ForeignKey("Form", related_name="fields")
    order = models.IntegerField(_("Order"), null=True, blank=True)

    class Meta(AbstractField.Meta):
        ordering = ("order",)

    def save(self, *args, **kwargs):
        if self.order is None:
            self.order = self.form.fields.count()
        super(Field, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        fields_after = self.form.fields.filter(order__gte=self.order)
        fields_after.update(order=models.F("order") - 1)
        super(Field, self).delete(*args, **kwargs)


@python_2_unicode_compatible
class FormItem(ContentItem):

    form = models.ForeignKey(Form)

    class Meta:
        verbose_name = _("Form")
        verbose_name_plural = _("Forms")

    def __str__(self):
        return self.form.title
