# Generated by Django 3.2.9 on 2021-11-09 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_wallettransactions_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallettransactions',
            name='type',
            field=models.CharField(default='credit', max_length=10),
            preserve_default=False,
        ),
    ]
