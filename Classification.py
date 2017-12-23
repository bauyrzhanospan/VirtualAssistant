#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from FNN.OrderClassifier.lib import modsGlobal as mO
from FNN.ReasonClassifier.lib import modsGlobal as mR


def classifyO(text):
    order = mO.classify(text)
    print(order)
    return order[0][0]


def classifyR(text):
    order = mR.classify(text)
    print(order)
    return order[0][0]
