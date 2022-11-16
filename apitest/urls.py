from django.urls import path
from django.views.static import serve

from django.views import static
from django.conf import settings
from django.conf.urls import url

from apitest.views import *

urlpatterns = [
    path('register/', register),
    path('index/', index),
    path('login/', LoginUser.as_view()),
    path('get_case/', get_case),
    path('debug_run_case/', debug_run_case),
    path('create_test_suite/', create_test_suite),
    path('all_suite/', all_suite),
    path('task_add_job/', task_add_job),
    path('remove_task/', remove_task),
    path('pause_task/', pause_task),
    path('get_all_job/', get_all_job),
    path('report/', Report.as_view()),
    path('add_case/', AddCase.as_view()),
    path('debug_case/', DebugCase.as_view()),
    path('add_job/', AddJob.as_view()),
    path('get_debug_case_report/', GetDebugCaseReport.as_view()),
    path('search_case/', SearchCase.as_view()),
    path('search_result/', SearchResult.as_view()),
    path('get_report/', GetReport.as_view()),

]
