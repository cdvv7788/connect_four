# Generated by Django 3.0.5 on 2020-05-01 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_auto_20200501_0247'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='started',
            field=models.BooleanField(default=False),
        ),
    ]