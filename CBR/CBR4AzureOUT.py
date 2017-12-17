import operator
import random
import time
import datetime
import pandas as pd
import scipy as sp
from scipy.spatial.distance import mahalanobis


prefList = {"energy": 0, "entertainment": 1, "food": 2, "health": 3, "security": 4, "work": 5}
usersList = {"adult": 0.6, "young": 0.3, "elder": 0.6}


def load():
    casesRaw = [{'output': 1, 'id': 0, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 1, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 2, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 3, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 4, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 5, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 6, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 7, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 8, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 9, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 10, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 11, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 12, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 13, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 14, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 15, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 16, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 17, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 18, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 19, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 20, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 21, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 22, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 23, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 24, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 25, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 26, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 27, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 28, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 0, 'id': 29, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 30, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 31, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 32, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 33, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 0, 'id': 34, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 35, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 36, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 37, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 38, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 0, 'id': 39, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 40, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 41, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 42, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 43, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 44, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 45, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 46, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 47, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 48, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 49, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 50, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 51, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 52, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 53, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 54, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 0, 'id': 55, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 56, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 57, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 58, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 59, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 60, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 61, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 62, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 63, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 64, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 65, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 66, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 67, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 68, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 69, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 70, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 71, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 72, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 73, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 74, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 75, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 76, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 77, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 78, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 79, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 80, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 81, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 82, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 83, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 84, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 85, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 86, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 87, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 88, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 89, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 90, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 91, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 92, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 93, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 94, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 95, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 96, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 97, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 98, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 99, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 100, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 101, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 102, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 103, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 104, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 105, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 106, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 107, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 108, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 109, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 110, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 111, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 112, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 113, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 114, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 115, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 116, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 117, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 118, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 119, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 120, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 121, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 122, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 123, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 124, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 125, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 126, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 127, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 128, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 129, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 130, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 131, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 132, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 133, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 134, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 135, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 136, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 137, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 138, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 139, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 140, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 141, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 142, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 143, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 144, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.3, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 145, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 146, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 147, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 148, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 149, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 150, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 151, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 152, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 153, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 154, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 155, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 156, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 157, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 158, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 159, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 160, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 161, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 162, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 163, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 164, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 165, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 166, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 167, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 168, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 169, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 170, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 171, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 172, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 173, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 0, 'id': 174, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.6},
                {'output': 1, 'id': 175, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 176, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 0, 'id': 177, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 178, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 179, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 180, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 181, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 0, 'id': 182, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 183, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 184, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 185, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 186, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 187, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 0, 'id': 188, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 189, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 190, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 191, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 192, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 193, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 194, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 195, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 196, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 197, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 198, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 199, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 200, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 201, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 0, 'id': 202, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 203, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3},
                {'output': 1, 'id': 204, 'reasonOUT': 1, 'reasonIN': 1, 'usertypeIN': 0.6, 'usertypeOUT': 0.3}]
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
    filename = "kingsout.txt"
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
            filename = "kingsout.txt"
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
