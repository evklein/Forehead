# Generated by Django 5.0.6 on 2024-06-30 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('round', '0006_remove_putt_hole_stats_remove_stroke_hole_stats_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stroke',
            name='distance',
        ),
        migrations.AlterField(
            model_name='stroke',
            name='start_coordinate',
            field=models.JSONField(null=True),
        ),
    ]