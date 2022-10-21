#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/10/11 13:11
# @Author  : heyangyang
# @FileName: KgPredict.py
# @Software: PyCharm

import json
import os

import sys
sys.path.append("../../../")

from KgAnswer import KgAnswer
from algorithm.kg_qa.config import NerConfig, SimConfig

from tornado import web
from tornado import ioloop

import time


class QAServer(web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        web.RequestHandler.__init__(self, application, request)
        self._kg = kwargs["kg_tool"]

    def get(self):
        """
        Get request
        """

    def post(self):
        time_start = time.clock()  # 记录开始时间

        input_request = self.request.body
        output = {}
        output['error_code'] = 0
        output['error_message'] = ''
        output['answer'] = []
        if input_request is None:
            output['error_code'] = 1
            output['error_message'] = "Input is empty"
            self.write(json.dumps(output))
            return

        try:
            input_data = json.loads(input_request)
        except:
            output['error_code'] = 2
            output['error_message'] = "Load input request error"
            self.write(json.dumps(output))
            return

        if "query" not in input_data:
            output['error_code'] = 3
            output['error_message'] = "[Query] is missing"
            self.write(json.dumps(output))
            return

        try:
            query = input_data['query']
            ans = self._kg.answer(query)
            output['answer'].append(ans[2] + '的' + ans[1] + '是' + ans[0] + '。')
            output['probs'] = ans[3]

            result_str = json.dumps(output, ensure_ascii=False)
            self.write(result_str)

            time_end = time.clock()  # 记录结束时间
            time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
            print("total time : ", time_sum)

            return
        except:
            output['error_code'] = 4
            output['error_message'] = "answer process error"
            self.write(json.dumps(output))
            return


def create_kgqa_app(sub_address, kg_server):
    """
    Create RocketQA server application
    """
    NER_MODEL_PATH = NerConfig.model_out
    SIM_MODEL_PATH = SimConfig.model_out
    es_host = "10.2.13.150"
    # es_host = "127.0.0.1"
    es_port = "9200"
    kg_ans = KgAnswer(NER_MODEL_PATH, SIM_MODEL_PATH, es_host, es_port)

    print('Load index done')

    return web.Application([(sub_address, kg_server, \
                             dict(kg_tool=kg_ans))])


if __name__ == "__main__":

    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    sub_address = r'/kgqa'
    port = '8000'
    app = create_kgqa_app(sub_address, QAServer)
    print("create kgqa app done")
    app.listen(port)
    print("app start listen port")
    ioloop.IOLoop.current().start()
