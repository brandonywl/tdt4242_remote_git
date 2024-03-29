# Generated by Django 3.1 on 2022-03-14 17:25

from django.db import migrations, models
import django.db.models.deletion
import meals.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('notes', models.TextField()),
                ('calories', models.IntegerField()),
                ('is_veg', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='MealFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=meals.models.meal_directory_path)),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='meals.meal')),
            ],
        ),
    ]
