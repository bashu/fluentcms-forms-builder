# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from fluent_contents.models.db import ContentItem
from forms_builder.forms.models import Form


@python_2_unicode_compatible
class FormItem(ContentItem):

    form = models.ForeignKey(Form)

    class Meta:
        verbose_name = _("Form")
        verbose_name_plural = _("Forms")

    def __str__(self):
        return self.form.title
