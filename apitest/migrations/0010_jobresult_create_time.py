# Generated by Django 3.2 on 2022-10-25 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0009_alter_jobresult_result_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobresult',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
