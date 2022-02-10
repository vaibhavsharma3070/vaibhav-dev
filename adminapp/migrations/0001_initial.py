# Generated by Django 2.2.10 on 2020-05-07 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('project_url', models.CharField(default='', max_length=100)),
                ('estimated_time', models.CharField(default='', max_length=100)),
                ('budget', models.DecimalField(decimal_places=2, default='0.0', max_digits=19)),
                ('short_description', models.TextField(default='')),
                ('description', models.TextField(default='')),
                ('state', models.CharField(default='In-progress', max_length=100)),
                ('similar_project', models.CharField(default='', max_length=150)),
                ('project_description', models.FileField(upload_to='')),
                ('tags_of_used_technology', models.CharField(default='', max_length=150)),
                ('main_major', models.CharField(default='', max_length=200)),
                ('progress', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('released_date', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(default='', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='project_created_by', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
        ),
        migrations.CreateModel(
            name='Responses',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(default='response', max_length=100)),
                ('response', models.TextField(default='')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('created_by', models.ForeignKey(default='', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='project_response_created', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='Project_response', to='adminapp.Projects')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectFilesAndImages',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='')),
                ('type', models.CharField(default='image', max_length=100)),
                ('subtype', models.CharField(default='secondary', max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('created_by', models.ForeignKey(default='', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='project_file_created', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='Project_file', to='adminapp.Projects')),
            ],
        ),
        migrations.CreateModel(
            name='Leads',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('similar_project', models.CharField(default='', max_length=150)),
                ('project_description', models.FileField(upload_to='')),
                ('main_major', models.CharField(default='', max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('state', models.CharField(default='In-progress', max_length=100)),
                ('created_by', models.ForeignKey(default='', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='lead_created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LeadFilesAndImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc', models.FileField(default='', upload_to='')),
                ('img', models.ImageField(default='', upload_to='')),
                ('lead', models.OneToOneField(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='Lead_file', to='adminapp.Leads')),
            ],
        ),
        migrations.CreateModel(
            name='Assignees',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('assigned_person', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='assigneed_person', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(default='', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='project_assignee_created', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='project_assignee', to='adminapp.Projects')),
            ],
        ),
    ]
