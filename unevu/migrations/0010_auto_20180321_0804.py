# Generated by Django 2.0.2 on 2018-03-21 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unevu', '0009_auto_20180321_0756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='imageUrl',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='mobile',
            field=models.CharField(max_length=14, null=True),
        ),
    ]
