# Generated by Django 4.1.7 on 2023-03-13 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cook',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=15, default=0, max_digits=19, null=True),
        ),
        migrations.AddField(
            model_name='cook',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=15, default=0, max_digits=19, null=True),
        ),
    ]
