#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os


class ProConfig(object):
    PROJECT_DIR = os.path.dirname(__file__)

    # tornado options
    options = {
        "ner_port": 8080,
        "sim_port": 8081,
        "simreq_port": 8082,
        "sim_port_list": '8081:8082:8083:8084',
        "query_port": 8089,
        "list": ["good", "nice", "handsome"]
    }
