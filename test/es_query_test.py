import sys
import requests
import json
from elasticsearch import Elasticsearch
import time
from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing as mp

time_start = time.time()  # 记录开始时间

entitys = '姚明'

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

attribute_list, answer_list = list(), list()
for i in range(len(es_results['hits']['hits'])):
    relation = es_results['hits']['hits'][i]['_source']['relation']
    value = es_results['hits']['hits'][i]['_source']['value']
    attribute_list.append(relation)
    answer_list.append(value)

print('attribute_list : ', attribute_list)
print('answer_list : ', answer_list)

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

if len(ambiguity_list) >= 5:
    ambiguity_list = ambiguity_list[0:5]

for i in range(len(ambiguity_list)):
    print('[', i, ']: ', ambiguity_list[i])

num = input('请选择您想了解的选项：')
ambiguity = ambiguity_list[int(num)]
print(ambiguity)

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

es_results = es.search(index="kbqa-data", doc_type="kbList", body=body, size=1000)

attribute_list, answer_list = list(), list()
for i in range(len(es_results['hits']['hits'])):
    relation = es_results['hits']['hits'][i]['_source']['relation']
    value = es_results['hits']['hits'][i]['_source']['value']
    attribute_list.append(relation)
    answer_list.append(value)

print('attribute_list : ', attribute_list)
print('answer_list : ', answer_list)

# time_end = time.clock()  # 记录结束时间
time_end = time.time()  # 记录结束时间
time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
print("es search time : ", time_sum)