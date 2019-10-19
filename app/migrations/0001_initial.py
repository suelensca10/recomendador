# Generated by Django 2.2.6 on 2019-10-19 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.IntegerField()),
                ('authors', models.CharField(max_length=500)),
                ('year', models.IntegerField()),
                ('title', models.CharField(max_length=500)),
                ('average_rating', models.FloatField()),
                ('ratings_count', models.FloatField()),
                ('ratings_1', models.FloatField()),
                ('ratings_2', models.FloatField()),
                ('ratings_3', models.FloatField()),
                ('ratings_4', models.FloatField()),
                ('ratings_5', models.FloatField()),
                ('image_url', models.FloatField()),
                ('small_image_url', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('rating', models.IntegerField()),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Book')),
            ],
        ),
    ]
