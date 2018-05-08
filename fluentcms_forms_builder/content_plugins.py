# -*- coding: utf-8 -*-

try:
    from django.core.context_processors import csrf
except ImportError:
    from django.template.context_processors import csrf
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.template import Context

from forms_builder.forms.views import FormDetail
from forms_builder.forms.signals import form_invalid, form_valid
from fluent_contents.extensions import ContentPlugin, plugin_pool

from .forms import FormForForm
from .models import FormItem


@plugin_pool.register
class FormPlugin(ContentPlugin):
    model = FormItem
    category = _('Form')
    render_template = "fluentcms_forms_builder/form.html"
    cache_output = False

    def get_context(self, request, instance, **kwargs):
        context = super(FormPlugin, self).get_context(
            request, instance, **kwargs)
        context.update(form=instance.form, **csrf(request))
        return context

    def render(self, request, instance, **kwargs):
        context = self.get_context(request, instance, **kwargs)

        form = instance.form
        if request.method == 'POST':
            form_for_form = FormForForm(
                form, Context(context), request.POST, request.FILES or None)

            if not form_for_form.is_valid():
                form_invalid.send(sender=request, form=form_for_form)
            else:
                attachments = []
                for f in form_for_form.files.values():
                    f.seek(0)
                    attachments.append((f.name, f.read()))

                entry = form_for_form.save()
                form_valid.send(sender=request, form=form_for_form, entry=entry)

                FormDetail().send_emails(request, form_for_form, form, entry, attachments)

                if not request.is_ajax() and form.redirect_url:
                    return redirect(str(form.redirect_url))

                return self.render_to_string(request, "fluentcms_forms_builder/form_sent.html", context)
        else:
            form_for_form = FormForForm(form, Context(context))

        context.update(form_for_form=form_for_form)

        return self.render_to_string(request, self.render_template, context)
