from apitest.models import JobResult


class SearchResultData(object):

    def search_result(self, case_name):
        res_data = JobResult.objects.filter(case_name=case_name)
        res = list(res_data.values("case_name", "result_id", "create_time"))
        return res
