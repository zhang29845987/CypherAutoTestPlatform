import json
import os
import subprocess
import sys
import time

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apitest.job_result import SearchResultData
from apitest.models import ApiCase, CaseSuit
from apitest.run_case import SQLRunCase, log_file_path
from apitest.task_pool import TaskPool
from autotestplatfrom.settings import BASE_DIR
from apitest.search_case import Search

TaskPool()


def register(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        User.objects.create_user(username=username, password=password)  # 密文密码
        return HttpResponse('ok')


@csrf_exempt
def login_user(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user_obj = auth.authenticate(request, username=username, password=password)
        if user_obj:
            auth.login(request, user_obj)
            return redirect('/index')
        else:
            return HttpResponse("登录失败")


class LoginUser(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        request_json_body = request.body
        request_json = json.loads(request_json_body)
        username = request_json["username"]
        password = request_json["password"]
        user_obj = auth.authenticate(request, username=username, password=password)
        if user_obj:
            # 保存用户状态信息(保存到session中)
            auth.login(request, user_obj)
            return JsonResponse({"msg": "0"})
        else:
            return JsonResponse({"msg": "1"})


@login_required(login_url="/login/")
def index(request):
    return render(request, 'index.html')


def get_case(request):
    if request.method == "GET":
        case_id = request.GET["case_id"]
        case_id = int(case_id)
        case_data = ApiCase.objects.get(pk=case_id)
        return JsonResponse(
            {"case_name": case_data.case_name, "case_data": case_data.case_code, "create_user": case_data.create_user})
    else:
        return JsonResponse({"status_message": "error"})


def debug_run_case(request):
    if request.method == "POST":
        case_id = request.POST["case_id"]
        case_data = ApiCase.objects.get(pk=case_id)
        # print(case_data.case_code)
        debug_file_name = str(BASE_DIR) + "/apitest/httprunner_api_test/testcases/" + "debug_" + str(
            case_data.pk) + "_" + case_data.case_name + ".yml"
        # TODO：增加如果文件存在那么就不需要进行写入操作
        # TODO: 增加数据的diff判断如果新请求的用户数据和最新的数据是一致的那么就不会做写入的操作
        report_file_name = "debug_" + str(case_data.pk) + "_" + str(time.time()) + ".html"
        report_file_path = str(BASE_DIR) + "/report/debug_report/" + report_file_name
        with open(debug_file_name, "w+") as file:
            file.write(case_data.case_code)
        p = subprocess.Popen(
            "hrun {file_path_} --html={report_file_path_} --self-contained-html".format(file_path_=debug_file_name,
                                                                                        report_file_path_=report_file_path),
            shell=True,
            # 命令行运行结果返回输出
            stdout=subprocess.PIPE,
            # 命令行运行出错返回输出
            stderr=subprocess.PIPE)
        p.stdout.read().decode("utf8")
        if os.path.exists(report_file_path):
            return render(request, report_file_name)


def create_test_suite(request):
    if request.method == "POST":
        suit_name = request.POST["suit_name"]
        if CaseSuit.objects.filter(suit_name__contains=suit_name).exists() is False:
            CaseSuit.objects.create(
                suit_name=suit_name
            )
            return JsonResponse(data={"msg": "OK"})
        else:
            return JsonResponse(data={"msg": "测试套件已经存在了请换个其他名字试试！"})


def all_suite(request):
    all_suite = CaseSuit.objects.all()
    return JsonResponse(data={"data": [suit_name.suit_name for suit_name in all_suite]})


def task_add_job(request):
    # 添加任务
    if request.method == "POST":
        case_id = request.POST["case_id"]
        interval_time = request.POST["interval_time"]
        TaskPool().add_job(case_id, int(interval_time))
        return JsonResponse({"message": "ok"})


def remove_task(request):
    # 删除任务
    if request.method == "POST":
        case_id = request.POST["case_id"]
        if case_id != '':
            TaskPool().remove_job(case_id)
            return JsonResponse({"message": "ok"})
        else:
            return JsonResponse({"message": "cannot be none"})


def pause_task(request):
    # 暂停任务
    if request.method == "POST":
        case_id = request.POST["case_id"]
        if case_id is not None or case_id is not "":
            TaskPool().pause_job(case_id)
            return JsonResponse({"message": "ok"})
        else:
            return JsonResponse({"message": "cannot be none"})


def resume_task(request):
    # 重启暂停任务
    if request.method == "POST":
        case_id = request.POST["job_id"]
        return HttpResponse("ok")


def get_all_job(request):
    if request.method == "GET":
        all_job = TaskPool().scheduler
        all_job.print_jobs(jobstore=None, out=sys.stdout)
        return JsonResponse({"message": "ok", "all_job": str(all_job)})


class Report(View):
    def get(self, request):
        result_id = request.GET.get("result_id")
        result_port_path = str(BASE_DIR) + f"/apitest/httprunner_api_test/logs/{result_id}.log"
        if os.path.isfile(result_port_path):
            with open(result_port_path) as f:
                return HttpResponse(f.read())
        else:
            return JsonResponse({"msg": "Not Fond log"})


class AddCase(View):
    def get(self, request):
        return render(request, "addcase.html")

    def post(self, request):
        try:
            request_json = json.loads(request.body)
            case_name = request_json["case_name"]
            case_code = request_json["case_code"]
            run_status = request_json["run_status"]
            suite_name = request_json["suite_name"]
            creator_name = request_json["creator"]
        except MultiValueDictKeyError:
            return JsonResponse({"status_message": "参数错误"})
        ApiCase.objects.create(
            case_name=case_name,
            case_code=case_code,
            run_status=run_status,
            create_user=creator_name
        )
        return JsonResponse({"status_code": "0", "msg": "success"})


class AddJob(View):
    def get(self, request):
        return render(request, "add_job.html")

    def post(self, request):
        # 添加任务
        if request.method == "POST":
            request_json = json.loads(request.body)
            case_id = request_json["case_id"]
            interval_time = request_json["interval_time"]
            TaskPool().add_job(int(case_id), int(interval_time))
            return JsonResponse({"status_code": "0", "message": "ok"})


class DebugCase(View):
    def post(self, request):
        request_json = json.loads(request.body)
        case_name = request_json["case_name"]
        case_code = request_json["case_code"]
        run = SQLRunCase()
        run.run_path(case_code, case_name)
        return JsonResponse({"status_code": "0", "result_id": run.result_id})


class GetDebugCaseReport(View):
    def get(self, request):
        result_id = request.GET["result_id"]
        log = log_file_path.format(_file_name=result_id)
        if os.path.isfile(log):
            with open(log, "r", encoding="utf-8") as file:
                log = file.read()
                return render(request, template_name="report.html", context={"log": log})


class SearchCase(View):
    def post(self, request):
        request_json = json.loads(request.body)
        search_content = request_json["search_content"]
        return JsonResponse({"status_code": "0", "case_list": Search().search_case(search_content)}, safe=True)


class SearchResult(View):
    def post(self, request):
        request_json = json.loads(request.body)
        case_name = request_json["case_name"]
        SearchResultData().search_result(case_name)
        return JsonResponse({"status_code": "0", "case_list": SearchResultData().search_result(case_name)}, safe=True)


class GetReport(View):
    def get(self, request):
        return render(request, "get_report.html")


def return_html_page(request):
    return HttpResponse("ok")
