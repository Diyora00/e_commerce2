# Generated by Django 5.0.7 on 2024-07-11 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='my_order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
