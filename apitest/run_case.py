import subprocess
import time
import uuid
from threading import Lock
import json
import yaml
from httprunner import HttpRunner
from httprunner.loader import load_testcase
from httprunner.models import TestCase
from apitest.models import ApiCase, JobResult
from autotestplatfrom.settings import BASE_DIR
from loguru import logger

api_case_dir_path = str(BASE_DIR) + "/apitest/httprunner_api_test/testcases/"
report_dir_path = str(BASE_DIR) + "/report/debug_report/"
# '/Users/bytedance/httprunner_test/logs/{_file_name}.log'.format(_file_name=log_file_name)
log_file_path = str(BASE_DIR) + "/apitest/httprunner_api_test/logs/{_file_name}.log"

lock = Lock()


# def run(case_id):
#     # 弃用
#     case_data = ApiCase.objects.get(pk=case_id)
#     api_case_path = api_case_dir_path + "debug_" + str(case_data.pk) + "_" + case_data.case_name + ".yml"
#     report_file_path = report_dir_path + "debug_" + str(case_data.pk) + "_" + str(time.time()) + ".html"
#     p = subprocess.Popen(
#         "hrun {file_path_} --html={report_file_path_} --self-contained-html".format(file_path_=api_case_path,
#                                                                                     report_file_path_=report_file_path),
#         shell=True,
#         # 命令行运行结果返回输出
#         stdout=subprocess.PIPE,
#         # 命令行运行出错返回输出
#         stderr=subprocess.PIPE)
#     return p.stdout.read().decode("utf8")

def run(case_code, case_name):
    SQLRunCase().run_path(case_code, case_name)


def load_case_code(case_code) -> TestCase:
    yaml_content = yaml.load(case_code, Loader=yaml.FullLoader)
    testcase_obj = load_testcase(yaml_content)
    return testcase_obj


class SQLRunCase(HttpRunner):
    result_id = None

    def run_path(self, case_code, case_name) -> "HttpRunner":
        # 不输出到控制台只输出到文件中
        lock.acquire()
        logger.remove(handler_id=None)
        result_id = str(uuid.uuid1())
        self.result_id = result_id
        # 自定义生成log文件
        logger.add(log_file_path.format(_file_name=result_id), enqueue=True)
        testcase_obj = load_case_code(case_code)
        testcase_obj.config.path = api_case_dir_path
        try:
            run_case_obj = self.run_testcase(testcase_obj)
        except Exception as e:
            pass
        lock.release()
        # logger.remove(log_handle_id)
        try:
            result_data = self.get_summary()
            result_data = result_data.json()
            result_data = json.loads(result_data)
        except Exception as e:
            result_data = {"success": False, "message": "error"}
        JobResult.objects.create(
            result_data=result_data,
            result_id=result_id,
            case_name=case_name,
            end_status=bool(result_data.get("success"))

        )


