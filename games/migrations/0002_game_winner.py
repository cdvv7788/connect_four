# Generated by Django 3.0.5 on 2020-04-30 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.BooleanField(default=None, null=True),
        ),
    ]
