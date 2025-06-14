# Generated by Django 5.1.6 on 2025-02-18 09:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(blank=True, null=True)),
                ('biography', models.TextField(blank=True, null=True)),
                ('total_books_published', models.PositiveIntegerField(default=0)),
                ('years_of_experience', models.FloatField(blank=True, null=True)),
                ('specialization', models.CharField(blank=True, max_length=255, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='author_profiles/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.login')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('profession', models.CharField(max_length=100)),
                ('bio', models.TextField(blank=True, null=True)),
                ('userprofile_image', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.login')),
            ],
        ),
    ]
