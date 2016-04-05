# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fluent_contents', '0001_initial'),
        ('forms', '0002_auto_20160405_0424'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormItem',
            fields=[
                ('contentitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem')),
                ('form', models.ForeignKey(to='forms.Form')),
            ],
            options={
                'db_table': 'contentitem_fluentcms_forms_builder_formitem',
                'verbose_name': 'Form',
                'verbose_name_plural': 'Forms',
            },
            bases=('fluent_contents.contentitem',),
        ),
    ]
