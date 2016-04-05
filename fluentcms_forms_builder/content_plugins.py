# -*- coding: utf-8 -*-

try:
    from django.core.context_processors import csrf
except ImportError:
    from django.template.context_processors import csrf
from django.utils.translation import ugettext_lazy as _

from fluent_contents.extensions import ContentPlugin, plugin_pool

from .models import FormItem


@plugin_pool.register
class FormPlugin(ContentPlugin):
    model = FormItem
    category = _('Form')
    render_template = "fluentcms_forms_builder/form.html"

    def get_context(self, request, instance, **kwargs):
        context = super(FormPlugin, self).get_context(
            request, instance, **kwargs)
        context.update(form=instance.form, **csrf(request))
        return context
