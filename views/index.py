#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/10/21 20:25
# @Author  : heyangyang
# @FileName: index.py
# @Software: PyCharm

import sys
from elasticsearch import Elasticsearch
from multiprocessing.dummy import Pool as ThreadPool

from tornado.web import RequestHandler
import json
import time
import requests


class NERHandler(RequestHandler):

    def __init__(self, application, request, **kwargs):
        RequestHandler.__init__(self, application, request)
        self._ner = kwargs["ner_tool"]

    def get(self):
        """
        Get request
        """

    def post(self):
        time_start = time.clock()  # 记录开始时间

        input_request = self.request.body
        output = {'error_code': 0, 'error_message': '', 'answer': []}
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
            entitys = "".join(self._ner.extract(query))
            output['answer'].append(entitys)

            result_str = json.dumps(output, ensure_ascii=False)
            self.write(result_str)

            time_end = time.clock()  # 记录结束时间
            time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
            print("ner time : ", time_sum)

            return
        except:
            output['error_code'] = 4
            output['error_message'] = "answer process error"
            self.write(json.dumps(output))
            return


class SIMHandler(RequestHandler):

    def __init__(self, application, request, **kwargs):
        RequestHandler.__init__(self, application, request)
        self._sim = kwargs["sim_tool"]

    def get(self):
        """
        Get request
        """

    def post(self):
        time_start = time.clock()  # 记录开始时间

        input_request = self.request.body
        # print(input_request)
        output = {'error_code': 0, 'error_message': '', 'answer': []}
        if input_request is None:
            output['error_code'] = 1
            output['error_message'] = "Input is empty"
            self.write(json.dumps(output))
            return

        try:
            input_data = json.loads(input_request)
            # print('sim input data : ', input_data)
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

        if "attribute" not in input_data:
            output['error_code'] = 3
            output['error_message'] = "[attribute] is missing"
            self.write(json.dumps(output))
            return

        try:
            sentence = input_data['query']
            attribute = input_data['attribute']
            isAttribute, probs = self._sim.predict_one(sentence, attribute, TEST_MODE=True)

            output['query'] = input_data['query']
            output['attribute'] = input_data['attribute']
            output['answer'] = input_data['answer']
            output['probs'] = str(probs[0][1])

            result_str = json.dumps(output, ensure_ascii=False)
            self.write(result_str)

            time_end = time.clock()  # 记录结束时间
            time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
            print("sim time : ", time_sum)

            return
        except:
            output['error_code'] = 4
            output['error_message'] = "answer process error"
            self.write(json.dumps(output))
            return


class SIMREQHandler(RequestHandler):

    def __init__(self, application, request, **kwargs):
        RequestHandler.__init__(self, application, request)
        self._SERVICE_ADD = 'http://10.2.13.150:8081/kg/sim'

    def get(self):
        """
        Get request
        """

    def post(self):
        # time_start = time.clock()  # 记录开始时间

        input_request = self.request.body
        output = {'error_code': 0, 'error_message': '', 'answer': []}
        if input_request is None:
            output['error_code'] = 1
            output['error_message'] = "Input is empty"
            self.write(json.dumps(output))
            return

        try:
            input_data = json.loads(input_request)
            # print('sim req input data : ', input_data)
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

        if "attribute" not in input_data:
            output['error_code'] = 3
            output['error_message'] = "[attribute] is missing"
            self.write(json.dumps(output))
            return

        if "answer" not in input_data:
            output['error_code'] = 3
            output['error_message'] = "[answer] is missing"
            self.write(json.dumps(output))
            return

        try:
            result = requests.post(self._SERVICE_ADD, json=input_data)
            # print(result)
            res_json = json.loads(result.text)

            output['query'] = input_data['query']
            output['attribute'] = input_data['attribute']
            output['answer'] = input_data['answer']
            output['probs'] = res_json['probs']

            result_str = json.dumps(output, ensure_ascii=False)
            self.write(result_str)

            # time_end = time.clock()  # 记录结束时间
            # time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
            # print("sim req time : ", time_sum)

            return
        except:
            output['error_code'] = 4
            output['error_message'] = "answer process error"
            self.write(json.dumps(output))
            return


class QUERYHandler(RequestHandler):

    def __init__(self, application, request, **kwargs):
        RequestHandler.__init__(self, application, request)

    def get(self):
        """
        Get request
        """

    def post(self):

        input_request = self.request.body
        output = {'error_code': 0, 'error_message': '', 'answer': []}
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

            entity = self.ner_request(query)

            if not entity:
                print('error: ner return None!')
                exit(0)

            # attribute_list, answer_list = self.es_search(entity)
            ambiguity_list, ambiguity_count = self.es_search1(entity)

            # if len(ambiguity_list) >= 5:
            #     ambiguity_list = ambiguity_list[0:5]
            #
            # for i in range(len(ambiguity_list)):
            #     print('[', i, ']: ', ambiguity_list[i])
            #
            # num = input('请选择您想了解的选项：')
            # ambiguity = ambiguity_list[int(num)]
            # print(ambiguity)

            if len(ambiguity_list) >= 1 and (ambiguity_list[0] is not None):
                ambiguity = ambiguity_list[0]
                attribute_list, answer_list = self.es_search2(entity, ambiguity)
            else:
                attribute_list, answer_list = self.es_search(entity)

            ans = self.sim_request3(query, attribute_list, answer_list)

            output['query'] = input_data['query']
            output['entity'] = entity
            output['attribute'] = ans[1]
            output['answer'] = ans[0]
            output['probs'] = ans[2]

            result_str = json.dumps(output, ensure_ascii=False)
            self.write(result_str)

            return
        except:
            output['error_code'] = 4
            output['error_message'] = "answer process error"
            self.write(json.dumps(output))
            return

    def req_process(self, item):

        input_data = {'query': item[0], 'attribute': item[1], 'answer': item[2]}
        base_url = 'http://10.2.13.150:' + str(item[3]) + '/kg/sim'
        result = requests.post(base_url, json=input_data)
        res_json = json.loads(result.text)

        return res_json

    def sim_request3(self, query, attribute_list, answer_list):

        best_answer = ""
        best_attribute = ""
        probs_init = 0

        sim_server_ports = [8081, 8082, 8083, 8084]

        input_d = []
        j = 0
        for i in range(len(attribute_list)):
            input_d.append([query, attribute_list[i], answer_list[i], sim_server_ports[j]])
            j += 1
            j = j % len(sim_server_ports)

        pool = ThreadPool(4)
        results = pool.map(self.req_process, input_d)
        pool.close()
        pool.join()

        for an in results:
            probs = float(an['probs'])
            if probs > probs_init:
                best_answer = an['answer']
                best_attribute = an['attribute']
                probs_init = probs

        ans = [best_answer, best_attribute, str(probs_init)]

        return ans

    def es_search(self, entitys):
        # es search
        # time_start = time.clock()  # 记录开始时间
        time_start = time.time()  # 记录开始时间

        body = {
            "query": {
                "term": {
                    "entity.keyword": entitys
                }
            }
        }

        es_host = "10.2.13.150"
        es_port = "9200"

        es = Elasticsearch([":".join((es_host, es_port))])
        es_results = es.search(index="kbqa-data", doc_type="kbList", body=body, size=1000)

        # time_end = time.clock()  # 记录结束时间
        time_end = time.time()  # 记录结束时间
        time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
        print("es search time : ", time_sum)

        attribute_list, answer_list = list(), list()
        for i in range(len(es_results['hits']['hits'])):
            relation = es_results['hits']['hits'][i]['_source']['relation']
            value = es_results['hits']['hits'][i]['_source']['value']
            attribute_list.append(relation)
            answer_list.append(value)

        print('attribute_list : ', attribute_list)
        print('answer_list : ', answer_list)

        return attribute_list, answer_list

    def es_search1(self, entitys):
        # es search

        body = {
            "query": {
                "term": {
                    "entity.keyword": entitys
                }
            },
            "size": 0,
            "aggs": {
                "ambiguity": {
                    "terms": {
                        "field": "ambiguity.keyword"
                    }
                }
            }
        }

        es_host = "10.2.13.150"
        es_port = "9200"

        es = Elasticsearch([":".join((es_host, es_port))])
        es_results = es.search(index="kbqa-data", doc_type="kbList", body=body, size=1000)

        ambiguity_list = []
        ambiguity_count = []
        for i in range(len(es_results['aggregations']['ambiguity']['buckets'])):
            ambiguity = es_results['aggregations']['ambiguity']['buckets'][i]['key']
            cnt = es_results['aggregations']['ambiguity']['buckets'][i]['doc_count']
            ambiguity_list.append(ambiguity)
            ambiguity_count.append(cnt)

        print('ambiguity_list : ', ambiguity_list)
        print('ambiguity_count : ', ambiguity_count)

        return ambiguity_list, ambiguity_count

    def es_search2(self, entitys, ambiguity):
        # es search

        body = {
                  "query": {
                    "bool": {
                      "must": [
                        {
                          "term": {
                            "entity.keyword": entitys
                          }
                        },
                        {
                          "term": {
                            "ambiguity.keyword": ambiguity
                          }
                        }
                      ]
                    }
                  }
                }

        es_host = "10.2.13.150"
        es_port = "9200"

        es = Elasticsearch([":".join((es_host, es_port))])
        es_results = es.search(index="kbqa-data", doc_type="kbList", body=body, size=1000)

        attribute_list, answer_list = list(), list()
        for i in range(len(es_results['hits']['hits'])):
            relation = es_results['hits']['hits'][i]['_source']['relation']
            value = es_results['hits']['hits'][i]['_source']['value']
            attribute_list.append(relation)
            answer_list.append(value)

        print('attribute_list : ', attribute_list)
        print('answer_list : ', answer_list)

        return attribute_list, answer_list

    def ner_request(self, query):

        # SERVICE_ADD = 'http://localhost:8080/ner'
        SERVICE_ADD = 'http://10.2.13.150:8080/kg/ner'

        input_data = {'query': query}

        # json_str = json.dumps(input_data).encode('utf-8').decode('unicode_escape')
        # print(json_str)

        result = requests.post(SERVICE_ADD, json=input_data)
        print('ner res : ', result)

        res_json = json.loads(result.text)
        print(res_json)

        if 'answer' not in res_json:
            return None
        else:
            entitys = res_json['answer'][0]

        return entitys

