from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CacheVersion",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("cache", models.CharField(max_length=128)),
                ("version", models.PositiveIntegerField(default=0)),
            ],
            options={},
            bases=(models.Model,),
        )
    ]
