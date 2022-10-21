import sys
import requests
import json
from elasticsearch import Elasticsearch
import time
from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing as mp


def ner_request(query):

    # SERVICE_ADD = 'http://localhost:8080/ner'
    SERVICE_ADD = 'http://10.2.13.150:8080/kg/ner'

    # query = input("please input a ner query:\t")
    # query = '任宪韶的毕业院校是?'
    # query = '姚明的职业是?'

    input_data = {}
    input_data['query'] = query

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


def es_search(entitys):
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
    # es_host = "127.0.0.1"
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


def sim_request(query, attribute_list, answer_list):

    best_answer = ""
    best_attribute = ""
    probs_init = 0

    # SERVICE_ADD = 'http://localhost:8080/sim'
    SERVICE_ADD = 'http://10.2.13.150:8081/kg/sim'

    for attribute, answer in zip(attribute_list, answer_list):
        if attribute:
            input_data = {}
            input_data['query'] = query
            input_data['attribute'] = attribute
            input_data['answer'] = answer
            # json_str = json.dumps(input_data).encode('utf-8').decode('unicode_escape')
            # print(json_str)

            result = requests.post(SERVICE_ADD, json=input_data)
            # print(result)
            res_json = json.loads(result.text)
            probs = float(res_json['probs'])
            if probs > probs_init:
                best_answer = answer
                best_attribute = attribute
                probs_init = probs

    ans = [best_answer, best_attribute, str(probs_init)]

    return ans


def sim_request2(query, attribute_list, answer_list):

    best_answer = ""
    best_attribute = ""
    probs_init = 0

    # SERVICE_ADD = 'http://localhost:8080/sim'
    SERVICE_ADD = 'http://10.2.13.150:8082/kg/simreq'

    for attribute, answer in zip(attribute_list, answer_list):
        if attribute:
            input_data = {}
            input_data['query'] = query
            input_data['attribute'] = attribute
            input_data['answer'] = answer
            # json_str = json.dumps(input_data).encode('utf-8').decode('unicode_escape')
            # print(json_str)

            result = requests.post(SERVICE_ADD, json=input_data)
            # print(result)
            res_json = json.loads(result.text)
            probs = float(res_json['probs'])
            if probs > probs_init:
                best_answer = answer
                best_attribute = attribute
                probs_init = probs

    ans = [best_answer, best_attribute, str(probs_init)]

    return ans


def sim_request3(query, attribute_list, answer_list):

    best_answer = ""
    best_attribute = ""
    probs_init = 0

    sim_server_ports = [8081, 8082, 8083, 8084]
    # sim_server_ports = [8085]

    input_d = []
    j = 0
    for i in range(len(attribute_list)):
        input_d.append([query, attribute_list[i], answer_list[i], sim_server_ports[j]])
        j += 1
        j = j % len(sim_server_ports)

    start = time.time()

    pool = ThreadPool(4)
    results = pool.map(req_process, input_d)
    pool.close()
    pool.join()

    print("Done in %d seconds, fetched %s items." % (time.time() - start, len(results)))

    for an in results:
        probs = float(an['probs'])
        if probs > probs_init:
            best_answer = an['answer']
            best_attribute = an['attribute']
            probs_init = probs

    ans = [best_answer, best_attribute, str(probs_init)]

    return ans


def req_process(item):

    input_data = {'query': item[0], 'attribute': item[1], 'answer': item[2]}
    base_url = 'http://10.2.13.150:' + str(item[3]) + '/kg/sim'
    result = requests.post(base_url, json=input_data)
    res_json = json.loads(result.text)

    return res_json


if __name__ == '__main__':
    query = '袁隆平的主要贡献是什么?'

    input_data = {'query': query}
    base_url = 'http://10.2.13.150:8089/kg/query'
    result = requests.post(base_url, json=input_data)
    res_json = json.loads(result.text)
    print(res_json)





    # entity = ner_request(query)

    # if not entity:
    #     print('error: ner return None!')
    #     exit(0)
    #
    # attribute_list, answer_list = es_search(entity)
    #
    # # time_start = time.clock()  # 记录开始时间
    # time_start = time.time()  # 记录开始时间
    # ans = sim_request3(query, attribute_list, answer_list)
    #
    # # time_end = time.clock()  # 记录结束时间
    # time_end = time.time()  # 记录结束时间
    # time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    # print("sim request time : ", time_sum)
    #
    # print("answer : ", entity + '的' + ans[1] + '是' + ans[0] + '。')
    # print('probs : ', ans[2])

#
#
# # sim query
# while True:
#     SERVICE_ADD = 'http://localhost:8080/sim'
#
#     query = input("please input a sim query:\t")
#
#     input_data = {}
#     input_data['query'] = query
#
#     attribute = input("please input a attribute:\t")
#     input_data['attribute'] = attribute
#
#     # input_data['query'] = '任宪韶的毕业院校是?'
#     json_str = json.dumps(input_data).encode('utf-8').decode('unicode_escape')
#     print(json_str)
#
#     result = requests.post(SERVICE_ADD, json=input_data)
#     print(result)
#     res_json = json.loads(result.text)
#
#     # print ("QUERY:\t" + input_data['query'])
#     print(res_json)
#
# # ner query
# while True:
#     SERVICE_ADD = 'http://localhost:8080/ner'
#
#     query = input("please input a ner query:\t")
#
#     input_data = {}
#     input_data['query'] = query
#     # input_data['query'] = '任宪韶的毕业院校是?'
#     json_str = json.dumps(input_data).encode('utf-8').decode('unicode_escape')
#     print(json_str)
#
#     result = requests.post(SERVICE_ADD, json=input_data)
#     print(result)
#     res_json = json.loads(result.text)
#
#     # print ("QUERY:\t" + input_data['query'])
#     print(res_json)

