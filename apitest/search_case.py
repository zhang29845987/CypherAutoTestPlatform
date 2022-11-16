"""
搜索case
"""
import json

from django.db.models import Q

from apitest.models import ApiCase


class Search(object):
    def search_case(self, content):
        res_data = ApiCase.objects.filter(Q(case_name__contains=content) | Q(create_user__contains=content))
        res = list(res_data.values("id", "case_name", "create_user", "create_time"))
        return res
