# Generated by Django 5.1.3 on 2024-11-20 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='id',
        ),
        migrations.AlterField(
            model_name='customer',
            name='username',
            field=models.TextField(primary_key=True, serialize=False),
        ),
    ]
