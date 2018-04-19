# Generated by Django 2.0 on 2018-01-12 06:31

from django.db import migrations, models
import tellme.models


class Migration(migrations.Migration):

    dependencies = [
        ('tellme', '0008_auto_20180112_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='Siteimage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('siteid', models.CharField(max_length=20)),
                ('picture', models.ImageField(upload_to=tellme.models.imageurl_handler)),
            ],
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
    ]
