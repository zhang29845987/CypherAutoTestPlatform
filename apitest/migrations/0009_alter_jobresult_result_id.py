# Generated by Django 3.2 on 2022-09-17 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0008_jobresult_end_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobresult',
            name='result_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
