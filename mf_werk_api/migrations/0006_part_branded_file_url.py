# Generated by Django 5.0.2 on 2024-02-22 16:25

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mf_werk_api', '0005_alter_part_designation_alter_part_drawing_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='branded_file_url',
            field=models.CharField(default=django.utils.timezone.now, max_length=180),
            preserve_default=False,
        ),
    ]
