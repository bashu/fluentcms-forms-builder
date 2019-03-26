# -*- coding: utf-8 -*-

from django.conf import settings

try:
    from django.core.context_processors import csrf
except ImportError:
    from django.template.context_processors import csrf
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.shortcuts import redirect

from email_extras.utils import send_mail_template

from forms_builder.forms.settings import EMAIL_FAIL_SILENTLY
from forms_builder.forms.signals import form_invalid, form_valid
from forms_builder.forms.utils import split_choices

from fluent_contents.extensions import ContentPlugin, plugin_pool

from .forms import FormForForm
from .models import FormItem, Form


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

        form = context['form']
        if request.method == 'POST':
            form_for_form = FormForForm(
                form, RequestContext(request), request.POST, request.FILES or None)

            if not form_for_form.is_valid():
                form_invalid.send(sender=request, form=form_for_form)
            else:
                attachments = []
                for f in form_for_form.files.values():
                    f.seek(0)
                    attachments.append((f.name, f.read()))

                entry = form_for_form.save()
                form_valid.send(sender=request, form=form_for_form, entry=entry)

                self.send_emails(request, form_for_form, form, entry, attachments)

                if not request.is_ajax() and form.redirect_url:
                    return redirect(str(form.redirect_url))

                return self.render_to_string(request, "fluentcms_forms_builder/form_sent.html", context)
        else:
            form_for_form = FormForForm(form, RequestContext(request))

        context.update(form_for_form=form_for_form)

        return self.render_to_string(request, self.render_template, context)

    def send_emails(self, request, form_for_form, form, entry, attachments):
        subject = form.email_subject
        if not subject:
            subject = "%s - %s" % (form.title, entry.entry_time)
        fields = []
        for (k, v) in form_for_form.fields.items():
            value = form_for_form.cleaned_data[k]
            if isinstance(value, list):
                value = ", ".join([i.strip() for i in value])
            fields.append((v.label, value))
        context = {
            "fields": fields,
            "message": form.email_message,
            "request": request,
        }
        email_from = form.email_from or settings.DEFAULT_FROM_EMAIL
        email_to = form_for_form.email_to()
        if email_to and form.send_email:
            send_mail_template(subject, "form_response", email_from,
                               email_to, context=context,
                               fail_silently=EMAIL_FAIL_SILENTLY)
        headers = None
        if email_to:
            headers = {"Reply-To": email_to}
        email_copies = split_choices(form.email_copies)
        if email_copies:
            send_mail_template(subject, "form_response_copies", email_from,
                               email_copies, context=context,
                               attachments=attachments,
                               fail_silently=EMAIL_FAIL_SILENTLY,
                               headers=headers)
