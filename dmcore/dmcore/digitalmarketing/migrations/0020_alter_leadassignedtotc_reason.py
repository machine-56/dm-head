# Generated by Django 5.1.6 on 2025-06-18 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitalmarketing', '0019_followupstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leadassignedtotc',
            name='reason',
            field=models.CharField(blank=True, default='No Data Availale', max_length=255, null=True),
        ),
    ]
