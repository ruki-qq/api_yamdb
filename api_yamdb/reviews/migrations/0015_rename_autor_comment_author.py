# Generated by Django 3.2 on 2023-11-30 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0014_rename_autor_review_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='autor',
            new_name='author',
        ),
    ]