# Generated by Django 3.2 on 2022-09-15 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0007_alter_jobresult_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobresult',
            name='end_status',
            field=models.BooleanField(default=False),
        ),
    ]