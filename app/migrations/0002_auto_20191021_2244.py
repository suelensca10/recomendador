# Generated by Django 2.2.6 on 2019-10-22 01:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='book_id',
            new_name='book',
        ),
    ]
