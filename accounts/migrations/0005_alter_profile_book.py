# Generated by Django 3.2.8 on 2021-10-22 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='book',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]