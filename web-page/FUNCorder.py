import nltk
from nltk.stem.lancaster import LancasterStemmer
import os
import json
import datetime
stemmer = LancasterStemmer()
import numpy as np
import time
import glob
from lib import modsOrder as mO
from lib import modsReason as mR

k = mO.classify("Turn on light")
b = mR.classify("I need a doctor")
print(k[0][0])
print(b[0][0])


