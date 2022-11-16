import uuid

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from apitest.models import ApiCase
from apitest.run_case import run


class TaskPool:
    # 任务
    scheduler = None
    # job_id
    job_id = None
    # 运行对象
    run_obj = None
    # None是一个空值，代表没有开辟空间
    __instance = None
    # 定义一个属性判断是否第一次走init方法
    __is__first = True
    executors = {
        'default': ThreadPoolExecutor(10),
        'processpool': ProcessPoolExecutor(50)
    }
    job_defaults = {
        'coalesce': True,
        'max_instances': 1,
        'misfire_grace_time': 15*60
    }

    def __init__(self):
        # 判断是否第一次
        # 此处需要保证只赋值一次，第二次开始创建对象时不会重新赋值，一直用第一个值
        if TaskPool.__is__first:
            # 单例模式主要解决的时任务执行器多次触发问题
            scheduler = BackgroundScheduler(timezone='Asia/Shanghai', executors=self.executors,
                                            job_defaults=self.job_defaults)
            scheduler.add_jobstore(DjangoJobStore(), 'default')
            scheduler.start()
            self.scheduler = scheduler
            # 设置类属性is__first为False
            TaskPool.__is__first = False

    # 重写new方法，是为了完成单例模式中的对象地址唯一
    def __new__(cls, *args, **kwargs):
        # 判断是否通过这个类创建过对象
        if not cls.__instance:
            # 如果not instance（即非None）
            cls.__instance = object.__new__(cls)
        return cls.__instance

    # 暂停任务
    def add_job(self, case_id, interval_time):
        case_data = ApiCase.objects.get(pk=case_id)
        self.job_id = str(case_data.pk) + str(case_data.case_name)
        self.scheduler.add_job(run, trigger='interval', seconds=interval_time, id=self.job_id,
                               args=[case_data.case_code, case_data.case_name])

    # 删除任务
    def remove_job(self, case_id):
        case_data = ApiCase.objects.get(pk=case_id)
        # case_id 等于case在数据库的主键id加case_name拼接而成
        job_id = str(case_data.pk) + str(case_data.case_name)
        self.scheduler.remove_job(job_id)

    # 暂停任务
    def pause_job(self, case_id):
        case_data = ApiCase.objects.get(pk=case_id)
        # case_id 等于case在数据库的主键id加case_name拼接而成
        job_id = str(case_data.pk) + str(case_data.case_name)
        self.scheduler.pause_job(job_id)

    def get_all_job(self):
        return self.scheduler.get_jobs()
