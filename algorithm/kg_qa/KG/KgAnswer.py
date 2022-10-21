#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os

import sys
import re
sys.path.append("../../../")

from elasticsearch import Elasticsearch

from algorithm.kg_qa.NER.EntityExtract import EntityExtract
from algorithm.kg_qa.SIM.Predict import Predict as SimPredict
from algorithm.kg_qa.config import NerConfig, SimConfig
import time

class KgAnswer(object):
    def __init__(self, NER_MODEL_PATH, SIM_MODEL_PATH, es_host, es_port):
        # init the model we need to use
        self.ee = EntityExtract(NER_MODEL_PATH)
        self.sim = SimPredict(SIM_MODEL_PATH)
        self.es = Elasticsearch([":".join((es_host, es_port))])

    def answer(self, sentence):

        time_start = time.clock()  # 记录开始时间

        entitys = "".join(self.ee.extract(sentence))
        # to_do 需要添加适配，多个实体的情况
        # print(entitys)

        time_end = time.clock()  # 记录结束时间
        time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
        print("model extract entitys time : ", time_sum)

        body = {
            "query": {
                "term": {
                    "entity.keyword": entitys
                }
            }
        }

        time_start = time.clock()  # 记录开始时间

        es_results = self.es.search(index="kbqa-data", doc_type="kbList", body=body, size=1000)

        time_end = time.clock()  # 记录结束时间
        time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
        print("es search time : ", time_sum)

        time_start = time.clock()  # 记录开始时间

        attribute_list, answer_list = list(), list()
        for i in range(len(es_results['hits']['hits'])):
            relation = es_results['hits']['hits'][i]['_source']['relation']
            value = es_results['hits']['hits'][i]['_source']['value']
            attribute_list.append(relation)
            answer_list.append(value)
        best_answer = ""
        best_attribute = ""
        probs_init = 0
        for attribute, answer in zip(attribute_list, answer_list):
            if attribute:
                isAttribute, probs = self.sim.predict_one(sentence, attribute, TEST_MODE=True)
                # if isAttribute:
                #     # print("问题：%s，属性：%s,回答：%s" % (sentence, attribute, answer))
                if probs[0][1] > probs_init:
                    best_answer = answer
                    best_attribute = attribute
                    probs_init = probs[0][1]

        time_end = time.clock()  # 记录结束时间
        time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
        print("model predict time : ", time_sum)

        return best_answer, best_attribute, entitys, str(probs_init)


if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    NER_MODEL_PATH = NerConfig.model_out
    SIM_MODEL_PATH = SimConfig.model_out
    es_host = "10.2.13.150"
    # es_host = "127.0.0.1"
    es_port = "9200"
    kg = KgAnswer(NER_MODEL_PATH, SIM_MODEL_PATH, es_host, es_port)
    print(kg.answer("NBA姚明学校在哪个地方啊？"))
    print(kg.answer("NBA姚明学校所属地区是？"))
    print(kg.answer("任宪韶的毕业院校是？"))
    sentence = "巫山县疾病预防控制中心的机构职能是什么?"
    print(kg.answer(sentence))
    # kg_out_f = open("./kg_out.txt", "w", encoding='utf-8')
    # with open(r"C:\Users\11943\Documents\GitHub\KgClue_Bench\raw_data\kgClue\test_public.json", 'r',
    #           encoding='utf-8') as f:
    #     count_number = 0
    #     true_answer = 0
    #     while True:
    #
    #         line = f.readline()
    #         if line:
    #             count_number += 1
    #             line = json.loads(line)
    #             sentence = line["question"]
    #             answer = line["answer"].split("|||")[2].strip()
    #             p_answers = kg.answer(sentence)
    #             # kg_out_f.write(sentence + "\t" + answer + "\t" + "predict: \t" + p_answers + "\n")
    #             # break
    #         else:
    #             break
    # kg_out_f.close()
