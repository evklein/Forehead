# Generated by Django 4.2.13 on 2024-06-26 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('round', '0002_rename_stroke_putt_stroke_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='nickname',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
