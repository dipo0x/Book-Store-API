# Generated by Django 3.2.8 on 2021-10-22 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_profile_total_downloads'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='book',
            field=models.IntegerField(default='12345'),
            preserve_default=False,
        ),
    ]
