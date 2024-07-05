# Generated by Django 5.0.6 on 2024-07-05 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('round', '0007_remove_stroke_distance_alter_stroke_start_coordinate'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='in_progress',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stroke',
            name='penalty',
            field=models.BooleanField(null=True),
        ),
    ]
