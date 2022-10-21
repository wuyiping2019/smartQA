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
from views.index import QUERYHandler


def create_kg_query_app(query_address, query_handler):
    """
    Create RocketQA server application
    """

    print('Load query server done')

    return tornado.web.Application([(query_address, query_handler)])


if __name__ == '__main__':
    # port = int(sys.argv[1])

    query_adds = r"/kg/query"
    app = create_kg_query_app(query_adds, QUERYHandler)
    print("create kg query app done")

    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.bind(ProConfig.options["query_port"])  # 从配置中获取端口
    # httpServer.bind(port)  # 从命令行中获取端口
    httpServer.start(1)

    print("app start listen query {} : {}".format(query_adds, ProConfig.options["query_port"]))
    tornado.ioloop.IOLoop.current().start()

