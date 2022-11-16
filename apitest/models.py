from django.db import models

# Create your models here.
from django_apscheduler.models import DjangoJobExecution


class ApiTest(models.Model):
    test_name = models.CharField(max_length=50)


class CaseSuit(models.Model):
    """
    主表
    """
    suit_name = models.CharField(max_length=50)


class ApiCase(models.Model):
    """
    子表
    """
    case_name = models.CharField(max_length=50, db_column="name")
    case_code = models.TextField(db_column="code")
    run_status = models.BooleanField(default=False)
    create_user = models.CharField(max_length=50)
    create_time = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    suit = models.ForeignKey(CaseSuit, on_delete=models.SET_NULL, null=True)


class JobResult(models.Model):
    result_data = models.TextField()
    result_id = models.CharField(max_length=100, null=True)
    case_name = models.CharField(max_length=50, null=True)
    end_status = models.BooleanField(default=False)
    create_time = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    class Meta:
        db_table = "job_results"

