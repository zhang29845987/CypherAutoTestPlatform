# Generated by Django 3.2 on 2022-09-04 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0003_apicase_create_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseSuit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suit_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='apicase',
            name='suit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='apitest.casesuit'),
        ),
    ]
