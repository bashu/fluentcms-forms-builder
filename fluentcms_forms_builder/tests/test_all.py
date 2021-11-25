from django.conf import settings
from django.urls import resolve
from django.core import mail
from django.template import RequestContext
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from fluent_contents.extensions import HttpRedirectRequest
from fluent_contents.tests.factories import create_content_item
from fluent_contents.tests.utils import render_content_items

from forms_builder.forms.fields import NAMES, TEXT, TEXTAREA, EMAIL
from forms_builder.forms.models import STATUS_DRAFT, STATUS_PUBLISHED
from fluentcms_forms_builder.models import Form, Field, FormItem
from fluentcms_forms_builder.forms import FormForForm


def get_dummy_request(method="get", **kwargs):
    """
    Returns a Request instance populated with cms specific attributes.
    """
    factory = RequestFactory()
    method = getattr(factory, method)

    request = method("/", HTTP_HOST="example.org", **kwargs)
    request.session = {}
    request.LANGUAGE_CODE = settings.LANGUAGE_CODE
    request.user = AnonymousUser()
    return request

class FormTests(TestCase):
    """
    Testing form plugin
    """

    def setUp(self):
        self.form = Form.objects.create(
            title="Contact Us", email_from="webmaster@example.org", email_message="message", status=STATUS_PUBLISHED)
        for (field, name) in {TEXT: "Subject", EMAIL: "Email", TEXTAREA: "Message"}.items():
            self.form.fields.create(label=name, field_type=field, required=True, visible=True)

    def test_rendering(self):
        """
        Test the standard form
        """
        item = create_content_item(FormItem, form=self.form)

        output = render_content_items([item])

        self.assertTrue(output.html.count('form action="."'), 1)
        self.assertTrue(output.html.count('name="form1-subject"'), 1)
        self.assertTrue(output.html.count('name="form1-email"'), 1)
        self.assertTrue(output.html.count('name="form1-message"'), 1)
        self.assertTrue(output.html.count('name="form1_submit"'), 1)

    def test_submit(self):
        """
        Testing submit
        """
        item = create_content_item(FormItem, form=self.form)

        # Submit, but not via the form button
        request = get_dummy_request("post", data={})
        request.resolver_match = resolve("/admin/")
        output = render_content_items([item], request=request)

        self.assertTrue(output.html.count('name="form1_submit"'), 1)  # still displays form
        self.assertTrue("error" not in output.html)  # no errors!

        # Submit, but not via the form button
        request = get_dummy_request(
            "post",
            data={
                "form1-subject": "Test!",
                "form1-email": "test@example.org",
                "form1-message": "Hello!",
                "form1_submit": "submit",
            },
        )
        request.resolver_match = resolve("/admin/")

        self.assertRaises(
            HttpRedirectRequest, lambda: render_content_items([item], request=request)
        )

    def test_email(self):
        """
        Test rendering the email
        """
        item = create_content_item(FormItem, form=self.form)

        # Submit, but not via the form button
        request = get_dummy_request(
            "post",
            data={
                "form1-subject": "Test!",
                "form1-email": "test@example.org",
                "form1-message": "Hello!",
                "form1_submit": "submit",
            },
        )
        request.resolver_match = resolve("/admin/")
        self.assertRaises(
            HttpRedirectRequest, lambda: render_content_items([item], request=request)
        )

        email = mail.outbox[0].body
        self.assertTrue("Message: Hello!" in email)
