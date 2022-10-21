#!/usr/bin/python3
# -*- coding: utf-8 -*-

def id2label(label_list):
    out = dict()
    for idx, label in enumerate(label_list):
        out[idx] = label
    return out
