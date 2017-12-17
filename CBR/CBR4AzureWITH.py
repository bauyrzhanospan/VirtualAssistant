import math
import operator
import random
import sys
import progressbar
import time
import datetime
import pymysql
import pandas as pd
import scipy as sp
from scipy.spatial.distance import mahalanobis

con = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user=None, passwd=None, db='virtass')
cur = con.cursor(pymysql.cursors.DictCursor)

prefList = {"energy": 0, "entertainment": 1, "food": 2, "health": 3, "security": 4, "work": 5}
usersList = {"adult": 0.6, "young": 0.3, "elder": 0.6}


def load():
    casesRaw = [{'id': 0, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.4, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 1, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.4, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 2, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.4, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 3, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.5, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 4, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.5, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 5, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.3, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 6, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.3, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 7, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.3, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 8, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.3, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 9, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.3, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 10, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.1, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 11, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.1, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 12, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.1, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 13, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.1, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 14, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.1, 'reasonOUT': 0.0, 'usertypeIN': 0.6},
                {'id': 15, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.1, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 16, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 17, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 18, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 19, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 20, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.2, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 21, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.2, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 22, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.2, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 23, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.2, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 24, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.2, 'reasonOUT': 0.0, 'usertypeIN': 0.6},
                {'id': 25, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.2, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 26, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.4, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 27, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.4, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 28, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.4, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 29, 'usertypeOUT': 0.3, 'output': 0, 'reasonIN': 0.4, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 30, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.4, 'reasonOUT': 0.0, 'usertypeIN': 0.6},
                {'id': 31, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.5, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 32, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.5, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 33, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.5, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 34, 'usertypeOUT': 0.3, 'output': 0, 'reasonIN': 0.5, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 35, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.5, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 36, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.3, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 37, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.3, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 38, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.3, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 39, 'usertypeOUT': 0.3, 'output': 0, 'reasonIN': 0.3, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 40, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.3, 'reasonOUT': 0.0, 'usertypeIN': 0.6},
                {'id': 41, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.3, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 42, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.1, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 43, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.1, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 44, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.1, 'reasonOUT': 0.0, 'usertypeIN': 0.6},
                {'id': 45, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.1, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 46, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 47, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 48, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 49, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 50, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.0, 'usertypeIN': 0.6},
                {'id': 51, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 52, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.2, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 53, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.2, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 54, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.2, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 55, 'usertypeOUT': 0.3, 'output': 0, 'reasonIN': 0.2, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 56, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.2, 'reasonOUT': 0.0, 'usertypeIN': 0.6},
                {'id': 57, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.2, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 58, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.4, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 59, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.4, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 60, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.4, 'reasonOUT': 0.0, 'usertypeIN': 0.6},
                {'id': 61, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.4, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 62, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.4, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 63, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.5, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 64, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.5, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 65, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.5, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 66, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.5, 'reasonOUT': 0.0, 'usertypeIN': 0.6},
                {'id': 67, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.5, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 68, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.5, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 69, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.3, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 70, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.3, 'reasonOUT': 0.0, 'usertypeIN': 0.6},
                {'id': 71, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.3, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 72, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.3, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 73, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.1, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 74, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.1, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 75, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.1, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 76, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.1, 'reasonOUT': 0.0, 'usertypeIN': 0.6},
                {'id': 77, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.1, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 78, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.1, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 79, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 80, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 81, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.0, 'usertypeIN': 0.6},
                {'id': 82, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 83, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.2, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 84, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.2, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 85, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.2, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 86, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.2, 'reasonOUT': 0.0, 'usertypeIN': 0.6},
                {'id': 87, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.2, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 88, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.2, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 89, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.5, 'reasonOUT': 0.4, 'usertypeIN': 0.3},
                {'id': 90, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.5, 'reasonOUT': 0.1, 'usertypeIN': 0.3},
                {'id': 91, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.5, 'reasonOUT': 0.0, 'usertypeIN': 0.3},
                {'id': 92, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.5, 'reasonOUT': 0.2, 'usertypeIN': 0.3},
                {'id': 93, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.2, 'reasonOUT': 0.4, 'usertypeIN': 0.3},
                {'id': 94, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.2, 'reasonOUT': 0.5, 'usertypeIN': 0.3},
                {'id': 95, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.2, 'reasonOUT': 0.3, 'usertypeIN': 0.3},
                {'id': 96, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.2, 'reasonOUT': 0.1, 'usertypeIN': 0.3},
                {'id': 97, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.2, 'reasonOUT': 0.0, 'usertypeIN': 0.3},
                {'id': 98, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.2, 'reasonOUT': 0.2, 'usertypeIN': 0.3},
                {'id': 99, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.4, 'reasonOUT': 0.3, 'usertypeIN': 0.3},
                {'id': 100, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.4, 'reasonOUT': 0.1, 'usertypeIN': 0.3},
                {'id': 101, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.4, 'reasonOUT': 0.0, 'usertypeIN': 0.3},
                {'id': 102, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.4, 'reasonOUT': 0.2, 'usertypeIN': 0.3},
                {'id': 103, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.3, 'reasonOUT': 0.4, 'usertypeIN': 0.3},
                {'id': 104, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.3, 'reasonOUT': 0.5, 'usertypeIN': 0.3},
                {'id': 105, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.3, 'reasonOUT': 0.3, 'usertypeIN': 0.3},
                {'id': 106, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.3, 'reasonOUT': 0.1, 'usertypeIN': 0.3},
                {'id': 107, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.3, 'reasonOUT': 0.0, 'usertypeIN': 0.3},
                {'id': 108, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.3, 'reasonOUT': 0.2, 'usertypeIN': 0.3},
                {'id': 109, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.0, 'reasonOUT': 0.4, 'usertypeIN': 0.3},
                {'id': 110, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.0, 'reasonOUT': 0.5, 'usertypeIN': 0.3},
                {'id': 111, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.0, 'reasonOUT': 0.3, 'usertypeIN': 0.3},
                {'id': 112, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.1, 'usertypeIN': 0.3},
                {'id': 113, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.0, 'reasonOUT': 0.0, 'usertypeIN': 0.3},
                {'id': 114, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.1, 'reasonOUT': 0.4, 'usertypeIN': 0.3},
                {'id': 115, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.1, 'reasonOUT': 0.5, 'usertypeIN': 0.3},
                {'id': 116, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.1, 'reasonOUT': 0.3, 'usertypeIN': 0.3},
                {'id': 117, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.1, 'reasonOUT': 0.1, 'usertypeIN': 0.3},
                {'id': 118, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.1, 'reasonOUT': 0.2, 'usertypeIN': 0.3},
                {'id': 119, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.5, 'reasonOUT': 0.4, 'usertypeIN': 0.3},
                {'id': 120, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.5, 'reasonOUT': 0.2, 'usertypeIN': 0.3},
                {'id': 121, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.5, 'reasonOUT': 0.0, 'usertypeIN': 0.3},
                {'id': 122, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.5, 'reasonOUT': 0.1, 'usertypeIN': 0.3},
                {'id': 123, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.2, 'reasonOUT': 0.3, 'usertypeIN': 0.3},
                {'id': 124, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.2, 'reasonOUT': 0.4, 'usertypeIN': 0.3},
                {'id': 125, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.2, 'reasonOUT': 0.2, 'usertypeIN': 0.3},
                {'id': 126, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.2, 'reasonOUT': 0.0, 'usertypeIN': 0.3},
                {'id': 127, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.4, 'reasonOUT': 0.3, 'usertypeIN': 0.3},
                {'id': 128, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.4, 'reasonOUT': 0.4, 'usertypeIN': 0.3},
                {'id': 129, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.4, 'reasonOUT': 0.2, 'usertypeIN': 0.3},
                {'id': 130, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.4, 'reasonOUT': 0.0, 'usertypeIN': 0.3},
                {'id': 131, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.4, 'reasonOUT': 0.1, 'usertypeIN': 0.3},
                {'id': 132, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.3, 'reasonOUT': 0.3, 'usertypeIN': 0.3},
                {'id': 133, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.3, 'reasonOUT': 0.4, 'usertypeIN': 0.3},
                {'id': 134, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.3, 'reasonOUT': 0.0, 'usertypeIN': 0.3},
                {'id': 135, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.3, 'reasonOUT': 0.1, 'usertypeIN': 0.3},
                {'id': 136, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.3, 'reasonOUT': 0.5, 'usertypeIN': 0.3},
                {'id': 137, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.0, 'reasonOUT': 0.3, 'usertypeIN': 0.3},
                {'id': 138, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.0, 'reasonOUT': 0.2, 'usertypeIN': 0.3},
                {'id': 139, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.0, 'usertypeIN': 0.3},
                {'id': 140, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.0, 'reasonOUT': 0.5, 'usertypeIN': 0.3},
                {'id': 141, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.1, 'reasonOUT': 0.3, 'usertypeIN': 0.3},
                {'id': 142, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.1, 'reasonOUT': 0.4, 'usertypeIN': 0.3},
                {'id': 143, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.1, 'reasonOUT': 0.2, 'usertypeIN': 0.3},
                {'id': 144, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.1, 'reasonOUT': 0.0, 'usertypeIN': 0.3},
                {'id': 145, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.3, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 146, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.3, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 147, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.3, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 148, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.3, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 149, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.3, 'reasonOUT': 0.0, 'usertypeIN': 0.6},
                {'id': 150, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.3, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 151, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.4, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 152, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.4, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 153, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.4, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 154, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.4, 'reasonOUT': 0.0, 'usertypeIN': 0.6},
                {'id': 155, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.4, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 156, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.2, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 157, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.2, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 158, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.2, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 159, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.2, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 160, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.2, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 161, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 162, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 163, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.0, 'usertypeIN': 0.6},
                {'id': 164, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.1, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 165, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.1, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 166, 'usertypeOUT': 0.6, 'output': 1, 'reasonIN': 0.1, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 167, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.1, 'reasonOUT': 0.0, 'usertypeIN': 0.6},
                {'id': 168, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.1, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 169, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.5, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 170, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.5, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 171, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.5, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 172, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.5, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 173, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.5, 'reasonOUT': 0.0, 'usertypeIN': 0.6},
                {'id': 174, 'usertypeOUT': 0.6, 'output': 0, 'reasonIN': 0.5, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 175, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.3, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 176, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.3, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 177, 'usertypeOUT': 0.3, 'output': 0, 'reasonIN': 0.3, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 178, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.3, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 179, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.4, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 180, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.4, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 181, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.4, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 182, 'usertypeOUT': 0.3, 'output': 0, 'reasonIN': 0.4, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 183, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.4, 'reasonOUT': 0.0, 'usertypeIN': 0.6},
                {'id': 184, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.4, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 185, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.2, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 186, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.2, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 187, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.2, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 188, 'usertypeOUT': 0.3, 'output': 0, 'reasonIN': 0.2, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 189, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.2, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 190, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 191, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 192, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 193, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 194, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.0, 'usertypeIN': 0.6},
                {'id': 195, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.0, 'reasonOUT': 0.1, 'usertypeIN': 0.6},
                {'id': 196, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.1, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 197, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.1, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 198, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.1, 'reasonOUT': 0.0, 'usertypeIN': 0.6},
                {'id': 199, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.5, 'reasonOUT': 0.5, 'usertypeIN': 0.6},
                {'id': 200, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.5, 'reasonOUT': 0.2, 'usertypeIN': 0.6},
                {'id': 201, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.5, 'reasonOUT': 0.4, 'usertypeIN': 0.6},
                {'id': 202, 'usertypeOUT': 0.3, 'output': 0, 'reasonIN': 0.5, 'reasonOUT': 0.3, 'usertypeIN': 0.6},
                {'id': 203, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.5, 'reasonOUT': 0.0, 'usertypeIN': 0.6},
                {'id': 204, 'usertypeOUT': 0.3, 'output': 1, 'reasonIN': 0.5, 'reasonOUT': 0.1, 'usertypeIN': 0.6}]
    training = casesRaw
    test = list(casesRaw[0::5])
    return training, test


def specy(weights, test):
    training, f = load()
    trainingRaw = []
    for mem in training:
        trainingRaw.append(mem["output"])

    for el in range(len(training)):
        del (training[el]["output"])
        del (training[el]["id"])
    del (test["output"])
    del (test["id"])

    for trainings in training:
        for key in trainings:
            trainings[key] = trainings[key] * weights[key]

    for key in test:
        test[key] = test[key] * weights[key]

    df = pd.DataFrame(training)
    covmx = df.cov()
    invcovmx = sp.linalg.inv(covmx)

    tests = [test["reasonIN"], test["reasonOUT"],
             test["usertypeIN"], test["usertypeOUT"]]

    distances = []
    for k in range(len(training)):
        trains = [training[k]["reasonIN"], training[k]["reasonOUT"],
                  training[k]["usertypeIN"], training[k]["usertypeOUT"]]
        distance = mahalanobis(trains, tests, invcovmx)
        distances.append([k, distance])

    classVotes = {}
    for x in range(len(distances)):
        response = distances[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(0), reverse=False)
    for el in distances:
        if el[1] == sortedVotes[0][0]:
            key = el[0]
            break
    response = trainingRaw[key]
    return response


def Accuracy(weights):
    training, test = load()
    acc = 0
    for el in range(len(test)):
        testing = test[el].copy()
        resp = specy(weights, testing)
        if resp == test[el]["output"]:
            acc = acc + 1
    return (acc / len(test)) * 100.0


def train():
    weights = {"usertypeIN": 1.0, "usertypeOUT": 1.0, "reasonIN": 1.0, "reasonOUT": 1.0}
    start_time = time.time()
    king = {"Epoch": 0, "Genome": weights, "Accuracy": float(Accuracy(weights))}
    speed = time.time() - start_time
    Epos = 800
    Deep = 3
    print("Number of epochs is " + str(Epos))
    print("Deepness of the analysis is " + str(Deep))
    execution_time = 1.1 * speed * Epos * Deep * int(200)
    print("Estimated execution time is " + str(datetime.timedelta(seconds=int(execution_time))))
    print("Estimated execution time for one epoch is " + str(
        datetime.timedelta(seconds=int(execution_time / 100000))))
    print("=======================================================================")
    print("Starting evolutional algorithm: ")
    bb = 0
    print("=======================================================================")
    print()
    print()
    print("Epoch num is 0")
    print("- - - - - - - - - - - - -")
    print("King is:")
    print(king)
    # Write the head of file
    filename = "kings.txt"
    with open(filename, 'a') as out:
        str1 = "Number of epochs is " + str(Epos) + "\n" + "Deepness of the analysis is " + str(Deep) + "\n" + \
               "Estimated execution time is " + str(datetime.timedelta(seconds=int(execution_time))) + "\n " + \
               "Genetic algorithms optimisation for KNN with preference weights" + "\n" + "=" * 20 + "\n"
        out.write(str1)

    # Execute GA
    genome = weights
    for epoha in range(Epos):
        organism = [king]
        for x in range(Deep):
            for k in range(100):
                new_weight = [float(i) * pow(10.0, -x) for i in [random.uniform(-1.0, 1.0) for _ in range(4)]]
                i = 0
                for key in genome:
                    genome[key] = genome[key] + new_weight[i]
                    i += 1
                organism.append({"Epoch": epoha, "Genome": genome, "Accuracy": float(Accuracy(genome))})
        prince = max(organism, key=lambda x: x['Accuracy'])
        if prince["Accuracy"] >= king["Accuracy"]:
            king = prince
            filename = "kings.txt"
            with open(filename, 'a') as out:
                out.write(str(king) + '\n')

        bb = 100 * epoha / Epos
        print("Percentage is: " + bb + " and accuracy is: " + str(king["Accuracy"]))
        # print(epoha)
        if king["Accuracy"] > 99.8:
            break
    print()
    print()
    print("=======================================================================")
    print()
    print()
    print("Epoch num is " + str(epoha))
    print("- - - - - - - - - - - - -")
    print("King is:")
    print(king)
    print("That is all!")
    with open(filename, 'a') as out:
        str1 = "=" * 20
        str1 = str1 + "Number of epochs is " + str(Epos) + "\n" + "Deepness of the analysis is " + str(Deep) + "\n" + \
               "Estimated execution time is " + str(datetime.timedelta(seconds=int(execution_time))) + "\n " + \
               "Genetic algorithms optimisation for KNN with preference weights" + "\n" + "The king is: \n" + str(king) \
               + "\n" + "=" * 20
        out.write(str1)


def main(usertypein, usertypeout, reasonin, reasonout):
    test = [str.lower(usertypein), str.lower(usertypeout), str.lower(reasonin), str.lower(reasonout)]
    return test


train()
