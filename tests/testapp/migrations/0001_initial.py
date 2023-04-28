import django.db.models.deletion
from django.db import migrations, models

import wagtail_site_inheritance.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("wagtailcore", "0041_group_collection_permissions_verbose_name_plural"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomePage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.Page",
                    ),
                ),
                ("body", models.CharField(default="", max_length=500)),
                ("custom_content", models.CharField(default="", max_length=500)),
            ],
            options={
                "abstract": False,
            },
            bases=(
                wagtail_site_inheritance.models.PageInheritanceMixin,
                "wagtailcore.page",
            ),
        ),
    ]
