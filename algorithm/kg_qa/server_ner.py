#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/10/21 20:25
# @Author  : heyangyang
# @FileName: server.py
# @Software: PyCharm

import os
import sys
sys.path.append("../../")

import re
from elasticsearch import Elasticsearch
from algorithm.kg_qa.NER.EntityExtract import EntityExtract
from algorithm.kg_qa.SIM.Predict import Predict as SimPredict
from algorithm.kg_qa.config import NerConfig, SimConfig
import time

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from proconfig import ProConfig
from views.index import NERHandler, SIMHandler, SIMREQHandler


def create_kg_ner_app(sub_address, ner_handler):
    """
    Create RocketQA server application
    """
    NER_MODEL_PATH = NerConfig.model_out
    kg_ner = EntityExtract(NER_MODEL_PATH)

    print('Load ner model done')

    return tornado.web.Application([(sub_address, ner_handler, \
                             dict(ner_tool=kg_ner))])

if __name__ == '__main__':
    # app = tornado.web.Application(
    #     [
    #         (r"/", NERHandler)
    #     ]
    # )

    # sub_adds = r"/ner"
    # app = create_kg_ner_app(sub_adds, NERHandler)
    # print("create kg ner app done")

    ner_adds = r"/kg/ner"
    app = create_kg_ner_app(ner_adds, NERHandler)
    print("create kg ner app done")

    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.bind(ProConfig.options["ner_port"])
    httpServer.start(1)

    print("app start listen ner {} : {}".format(ner_adds, ProConfig.options["ner_port"]))
    tornado.ioloop.IOLoop.current().start()
