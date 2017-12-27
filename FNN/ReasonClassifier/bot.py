#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import nltk
from nltk.stem.lancaster import LancasterStemmer
import os
import json
import datetime

stemmer = LancasterStemmer()
import numpy as np
import time
from lib import mods as m


while 1:
    data = input("Your reason is: ")
    # m.classify(data)
    print("Output vector for your reason classification is: ")
    k = m.classify(data)
    # print(k[0][0])
