# Generated by Django 2.2.6 on 2019-10-24 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20191023_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image_file',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
