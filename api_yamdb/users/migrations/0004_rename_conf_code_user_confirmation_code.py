# Generated by Django 3.2 on 2023-12-01 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_confirmation_code_user_conf_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='conf_code',
            new_name='confirmation_code',
        ),
    ]
