# Generated by Django 2.2.6 on 2019-11-01 01:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_book_image_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='book',
            new_name='book_id',
        ),
    ]
