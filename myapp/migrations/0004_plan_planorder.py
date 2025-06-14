# Generated by Django 5.1.6 on 2025-02-19 05:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_category_book'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('plan_type', models.CharField(choices=[('Standard', 'Standard'), ('Premium', 'Premium')], max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('duration_months', models.IntegerField()),
                ('description', models.TextField()),
                ('max_books_per_month', models.IntegerField(default=0, help_text='Number of books a user can access per month')),
                ('can_listen_audio', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlanOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razorpay_order_id', models.CharField(blank=True, max_length=255, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=255, null=True)),
                ('razorpay_signature', models.CharField(blank=True, max_length=255, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Failed', 'Failed')], default='Pending', max_length=20)),
                ('purchase_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('expiration_date', models.DateTimeField(blank=True, null=True)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.plan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.login')),
            ],
        ),
    ]
