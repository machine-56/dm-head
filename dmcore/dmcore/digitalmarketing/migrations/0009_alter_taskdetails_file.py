# Generated by Django 5.1.6 on 2025-05-22 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitalmarketing', '0008_taskdetails_achieved_target'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskdetails',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='daily_work/files/'),
        ),
    ]
