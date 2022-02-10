# Generated by Django 3.0.4 on 2022-02-04 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0013_auto_20220204_1808'),
    ]

    operations = [
        migrations.CreateModel(
            name='Button',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('page_title', models.CharField(max_length=100)),
                ('url', models.CharField(blank=True, max_length=100, null=True)),
                ('isAvailable_indicator', models.BooleanField()),
                ('isSlider_available', models.BooleanField()),
                ('isNew_flag', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=100)),
                ('language_code', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('button_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='button_obj', to='adminapp.Button')),
            ],
        ),
    ]
