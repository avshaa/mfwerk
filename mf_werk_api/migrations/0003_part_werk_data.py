# Generated by Django 5.0.2 on 2024-02-11 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mf_werk_api', '0002_part_org_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='werk_data',
            field=models.CharField(default='', max_length=13600),
        ),
    ]
