# Generated by Django 5.1.3 on 2024-12-07 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_screen', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='id',
        ),
        migrations.AlterField(
            model_name='customer',
            name='id_number',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
