# Generated by Django 5.1.3 on 2024-11-20 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0003_remove_passwordhistory_user_delete_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.TextField()),
                ('email', models.TextField()),
                ('password', models.TextField()),
            ],
        ),
    ]
