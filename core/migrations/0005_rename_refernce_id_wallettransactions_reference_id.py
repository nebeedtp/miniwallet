# Generated by Django 3.2.9 on 2021-11-09 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_wallettransactions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wallettransactions',
            old_name='refernce_id',
            new_name='reference_id',
        ),
    ]
