# Generated by Django 3.0.5 on 2020-05-07 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0006_auto_20200503_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('STARTED', 'Started'), ('FINISHED', 'Finished')], default='PENDING', max_length=8),
        ),
    ]
