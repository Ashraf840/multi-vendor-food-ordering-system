# Generated by Django 3.2.8 on 2021-11-19 12:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, null=True)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profilePicture')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Profile',
            },
        ),
        migrations.CreateModel(
            name='RestaurantProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opening_time', models.TimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('closing_time', models.TimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('is_closed', models.BooleanField(default=False)),
                ('restaurant_profile_pic', models.ImageField(blank=True, default='rProfilePicture/default_rest_dp.jpg', null=True, upload_to='rProfilePicture')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Date Created')),
                ('last_updated_at', models.DateField(auto_now_add=True, verbose_name='Last Updated')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Restaurant Profile',
            },
        ),
    ]
