# Generated by Django 3.2.8 on 2021-11-19 12:00

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Addon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addon_name', models.CharField(max_length=100, null=True)),
                ('price', models.FloatField()),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Date Created')),
                ('last_updated_at', models.DateField(auto_now_add=True, verbose_name='Last Updated')),
                ('is_available', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rest-owner+', to=settings.AUTH_USER_MODEL, verbose_name='Restaurant Owner')),
            ],
            options={
                'verbose_name_plural': 'Food Addon',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cate_name', models.CharField(max_length=50, null=True)),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Date Created')),
                ('last_updated_at', models.DateField(auto_now_add=True, verbose_name='Last Updated')),
            ],
            options={
                'verbose_name_plural': 'Food Category',
            },
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(max_length=100, null=True)),
                ('reward_point', models.PositiveSmallIntegerField(default=1)),
                ('price', models.FloatField()),
                ('food_code', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('image', models.FileField(blank=True, default='foodImage/default_food_image.png', upload_to='foodImage')),
                ('total_viewed', models.PositiveBigIntegerField(default=0)),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Date Created')),
                ('last_updated_at', models.DateField(auto_now_add=True, verbose_name='Last Updated')),
                ('is_available', models.BooleanField(default=True)),
                ('addon', models.ManyToManyField(blank=True, to='food.Addon')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='food.category')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rest-owner+', to=settings.AUTH_USER_MODEL, verbose_name='Restaurant Owner')),
            ],
            options={
                'verbose_name_plural': 'Food',
            },
        ),
        migrations.CreateModel(
            name='FoodReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_msg', models.TextField(help_text='Write a review')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Date Created')),
                ('last_updated_at', models.DateField(auto_now_add=True, verbose_name='Last Updated')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer-id+', to=settings.AUTH_USER_MODEL, verbose_name='Customer')),
                ('food_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food-id+', to='food.food', verbose_name='Food')),
            ],
            options={
                'verbose_name_plural': 'Food Review (by Customer)',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=50, null=True, unique=True)),
                ('date_created', models.DateField(auto_now_add=True, verbose_name='Date Created')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Food Tag',
            },
        ),
        migrations.CreateModel(
            name='ReviewHelpful',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_helpful', models.BooleanField(default=True)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer-id+', to=settings.AUTH_USER_MODEL, verbose_name='Customer')),
                ('review_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review-id+', to='food.foodreview', verbose_name='Review')),
            ],
            options={
                'verbose_name_plural': 'Food Review Helpful (Positive/ Negative)',
            },
        ),
        migrations.CreateModel(
            name='FoodRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Date Created')),
                ('last_updated_at', models.DateField(auto_now_add=True, verbose_name='Last Updated')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer-id+', to=settings.AUTH_USER_MODEL, verbose_name='Customer')),
                ('food_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food-id+', to='food.food', verbose_name='Food')),
            ],
            options={
                'verbose_name_plural': 'Food Rating (by Customer)',
            },
        ),
        migrations.CreateModel(
            name='FoodLikes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Date Created')),
                ('last_updated_at', models.DateField(auto_now_add=True, verbose_name='Last Updated')),
                ('is_liked', models.BooleanField(default=True)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer-id+', to=settings.AUTH_USER_MODEL, verbose_name='Customer')),
                ('food_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food-id+', to='food.food', verbose_name='Food')),
            ],
            options={
                'verbose_name_plural': 'Food Like',
            },
        ),
        migrations.AddField(
            model_name='food',
            name='tag',
            field=models.ManyToManyField(blank=True, to='food.Tag'),
        ),
        migrations.CreateModel(
            name='ComboMeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('combo_name', models.CharField(max_length=100, null=True, verbose_name='Combo Meal Name')),
                ('price', models.FloatField()),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Date Created')),
                ('last_updated_at', models.DateField(auto_now_add=True, verbose_name='Last Updated')),
                ('is_available', models.BooleanField(default=True)),
                ('RO_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer-id+', to=settings.AUTH_USER_MODEL, verbose_name='Restaurant')),
                ('food_id', models.ManyToManyField(blank=True, to='food.Food')),
            ],
            options={
                'verbose_name_plural': 'Combo Meal',
            },
        ),
    ]
