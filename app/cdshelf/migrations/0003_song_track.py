# Generated by Django 5.1 on 2024-08-28 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cdshelf", "0002_alter_sourcedir_location"),
    ]

    operations = [
        migrations.AddField(
            model_name="song",
            name="track",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
