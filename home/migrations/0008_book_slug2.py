# Generated by Django 3.2.8 on 2021-10-21 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_remove_book_slug2'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='slug2',
            field=models.CharField(default='"87443"', max_length=7),
            preserve_default=False,
        ),
    ]
