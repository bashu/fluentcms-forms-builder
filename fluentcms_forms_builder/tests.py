from django.test import TestCase
from fluent_contents.tests.factories import create_content_item
from fluent_contents.tests.utils import get_dummy_request, render_content_items

from forms_builder.forms.fields import NAMES, TEXT, TEXTAREA, EMAIL
from forms_builder.forms.models import STATUS_DRAFT, STATUS_PUBLISHED
from fluentcms_forms_builder.models import Form, Field, FormItem


class FormTests(TestCase):
    """
    Testing form plugin
    """

    def test_rendering(self):
        """
        Test the standard form
        """
        form = Form.objects.create(title="Test", status=STATUS_PUBLISHED)
        for (field, _) in NAMES:
            if not field in (TEXT, TEXTAREA, EMAIL):
                continue
            form.fields.create(label=field, field_type=field, required=False, visible=True)

        item = create_content_item(FormItem, form=form)
        output = render_content_items([item])

        self.assertTrue(output.html.count('form action="."'), 1)
        self.assertTrue(output.html.count('type="text"'), 1)
        self.assertTrue(output.html.count('textarea'), 1)
        self.assertTrue(output.html.count('type="email"'), 1)
        self.assertTrue(output.html.count('input type="submit"'), 1)

    def test_submit(self):
        pass

    def test_email(self):
        pass
