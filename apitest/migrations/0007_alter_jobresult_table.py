# Generated by Django 3.2 on 2022-09-15 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0006_jobresult_case_name'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='jobresult',
            table='job_results',
        ),
    ]
