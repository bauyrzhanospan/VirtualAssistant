# use natural language toolkit
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
    data = input("What:")
    #m.classify(data)
    k = m.classify(data)
    print(k[0][0])