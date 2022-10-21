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


def create_kg_sim_app(sim_address, sim_handler):
    """
    Create RocketQA server application
    """
    SIM_MODEL_PATH = SimConfig.model_out
    kg_sim = SimPredict(SIM_MODEL_PATH)
    print('Load sim model done')

    return tornado.web.Application([(sim_address, sim_handler, \
                             dict(sim_tool=kg_sim))])


if __name__ == '__main__':
    port = int(sys.argv[1])

    sim_adds = r"/kg/sim"
    app = create_kg_sim_app(sim_adds, SIMHandler)
    print("create kg sim app done")

    httpServer = tornado.httpserver.HTTPServer(app)
    # httpServer.bind(ProConfig.options["sim_port"])  # 从配置中获取端口
    httpServer.bind(port)  # 从命令行中获取端口
    httpServer.start(1)

    print("app start listen sim {} : {}".format(sim_adds, port))
    tornado.ioloop.IOLoop.current().start()

