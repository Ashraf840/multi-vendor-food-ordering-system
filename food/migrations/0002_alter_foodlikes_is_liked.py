# Generated by Django 3.2.8 on 2021-12-04 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodlikes',
            name='is_liked',
            field=models.BooleanField(default=False),
        ),
    ]
