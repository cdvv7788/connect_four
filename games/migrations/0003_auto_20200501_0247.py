# Generated by Django 3.0.5 on 2020-05-01 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_game_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='player_1',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='game',
            name='player_2',
            field=models.CharField(default='', max_length=30),
        ),
    ]
