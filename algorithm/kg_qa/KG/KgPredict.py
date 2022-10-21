#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os

import sys
import re
sys.path.append("../../../")

from KgAnswer import KgAnswer
from algorithm.kg_qa.config import NerConfig, SimConfig

if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    NER_MODEL_PATH = NerConfig.model_out
    SIM_MODEL_PATH = SimConfig.model_out
    es_host = "10.2.13.150"
    # es_host = "127.0.0.1"
    es_port = "9200"
    kg = KgAnswer(NER_MODEL_PATH, SIM_MODEL_PATH, es_host, es_port)

    sentence = "NBA姚明学校在哪个地方啊?"
    print("question : ", sentence)
    ans = kg.answer(sentence)
    print("answer : ", ans[2] + '的' + ans[1] + '是' + ans[0] + '。')

    sentence = "NBA姚明学校所属地区是?"
    print("question : ", sentence)
    ans = kg.answer(sentence)
    print("answer : ", ans[2] + '的' + ans[1] + '是' + ans[0] + '。')

    sentence = "任宪韶的毕业院校是?"
    print("question : ", sentence)
    ans = kg.answer(sentence)
    print("answer : ", ans[2] + '的' + ans[1] + '是' + ans[0] + '。')

    sentence = "巫山县疾病预防控制中心的机构职能是什么?"
    print("question : ", sentence)
    ans = kg.answer(sentence)
    print("answer : ", ans[2] + '的' + ans[1] + '是' + ans[0] + '。')

    # print(kg.answer("NBA姚明学校在哪个地方啊？"))
    # print(kg.answer("NBA姚明学校所属地区是？"))
    # print(kg.answer("任宪韶的毕业院校是？"))
    # sentence = "巫山县疾病预防控制中心的机构职能是什么?"
    # print(kg.answer(sentence))

    # out_f = open("./kgclue_predict.txt", "w", encoding='utf-8')
    # with open(r"C:\Users\11943\Documents\GitHub\KgCLUEbench\raw_data\kgClue\test.json", 'r', encoding='utf-8') as f:
    #     count_number = 0
    #     while True:
    #
    #         line = f.readline()
    #         if line:
    #
    #             line = json.loads(line)
    #             sentence = line["question"]
    #             best_answer, best_attribute, entitys = kg.answer(sentence)
    #             tmp = dict()
    #             tmp["id"] = count_number
    #             tmp["answer"] = str(entitys) + " ||| " + str(best_attribute) + " ||| " + str(best_answer)
    #             x = json.dumps(tmp, ensure_ascii=False)
    #             out_f.write(x+"\n")
    #             # print(x)
    #             count_number += 1
    #             # break
    #             # {"id": 0, "answer": "刘质平 ||| 师从 ||| 李叔同"}
    #
    #         else:
    #             break
    # out_f.close()
