from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fluent_contents", "0001_initial"),
        ("forms", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FormItem",
            fields=[
                (
                    "contentitem_ptr",
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        to="fluent_contents.ContentItem",
                        on_delete=models.CASCADE,
                    ),
                ),
                ("form", models.ForeignKey(to="forms.Form", on_delete=models.CASCADE)),
            ],
            options={
                "db_table": "contentitem_fluentcms_forms_builder_formitem",
                "verbose_name": "Form",
                "verbose_name_plural": "Forms",
            },
            bases=("fluent_contents.contentitem",),
        ),
    ]
