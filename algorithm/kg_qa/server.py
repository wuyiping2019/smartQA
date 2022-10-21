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


def create_kg_app(ner_address, sim_address, simreq_adds, ner_handler, sim_handler, simreq_handler):
    """
    Create RocketQA server application
    """
    NER_MODEL_PATH = NerConfig.model_out
    kg_ner = EntityExtract(NER_MODEL_PATH)
    print('Load ner model done')

    SIM_MODEL_PATH = SimConfig.model_out
    kg_sim = SimPredict(SIM_MODEL_PATH)
    print('Load sim model done')

    return tornado.web.Application([(ner_address, ner_handler, \
                             dict(ner_tool=kg_ner)),
                                    (sim_address, sim_handler, \
                             dict(sim_tool=kg_sim)),
                                    (simreq_adds, simreq_handler)])


if __name__ == '__main__':
    # app = tornado.web.Application(
    #     [
    #         (r"/", NERHandler)
    #     ]
    # )

    # sub_adds = r"/ner"
    # app = create_kg_ner_app(sub_adds, NERHandler)
    # print("create kg ner app done")

    ner_adds = r"/ner"
    sim_adds = r"/sim"
    simreq_adds = r"/simreq"
    app = create_kg_app(ner_adds, sim_adds, simreq_adds, NERHandler, SIMHandler, SIMREQHandler)
    print("create kg ner sim simreq app done")

    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.bind(ProConfig.options["port"])
    httpServer.start(1)

    print("app start listen ner {} : {}".format(ner_adds, ProConfig.options["port"]))
    print("app start listen sim {} : {}".format(sim_adds, ProConfig.options["port"]))
    print("app start listen simreq {} : {}".format(simreq_adds, ProConfig.options["port"]))
    tornado.ioloop.IOLoop.current().start()
