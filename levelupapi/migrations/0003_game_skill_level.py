# Generated by Django 3.2.6 on 2021-08-06 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0002_auto_20210803_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='skill_level',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
