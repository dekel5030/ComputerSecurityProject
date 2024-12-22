# Generated by Django 5.1.3 on 2024-12-08 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_password_history_username_delete_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('id_number', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('phone_number', models.CharField(max_length=11)),
                ('city', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('package', models.CharField(max_length=50)),
            ],
        ),
    ]
