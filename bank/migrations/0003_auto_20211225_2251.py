# Generated by Django 3.2.9 on 2021-12-25 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0002_atm'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atm',
            name='pin_no',
        ),
        migrations.AddField(
            model_name='atm',
            name='name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='atm',
            name='pinno',
            field=models.CharField(default='1234', max_length=4),
        ),
    ]