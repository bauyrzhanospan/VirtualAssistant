import pymysql
import random


def importprefs():
    con = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user=None, passwd=None, db='virtass')
    cur = con.cursor(pymysql.cursors.DictCursor)
    dataset = {}
    with con:
        cur.execute('SELECT * FROM preferences')
        dataset = cur.fetchall()
    return dataset


def importcases():
    con = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user=None, passwd=None, db='virtass')
    cur = con.cursor(pymysql.cursors.DictCursor)
    dataset = {}
    with con:
        cur.execute('SELECT * FROM cases')
        dataset = cur.fetchall()
    return dataset


con = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user=None, passwd=None, db='virtass')
cur = con.cursor()
cur.execute("TRUNCATE TABLE cases")
con.commit()

dataset = importprefs()
cases = importcases()

usertypes = ["adult", "young", "elder"]
userweights = {"adult": 1, "young": 3, "elder": 2}
reasons = ["energy", "entertainment", "food", "health", "security", "work"]

start = "INSERT INTO `cases` (`id`, `usertypeIN`, `usertypeOUT`, `reasonIN`, `reasonOUT`, `output`) VALUES ('"

divider = "', '"
m = 0
k = 0
for el in usertypes:
    for oel in usertypes:
        if el != oel or (el == oel and el == "adult"):
            for re in reasons:
                for res in reasons:
                    user1 = el
                    user2 = oel
                    reason1 = re
                    reason2 = res
                    value = 0
                    for thn in dataset:
                        if thn["usertype"] == user1:
                            reason1w = thn[reason1]
                        if thn["usertype"] == user2:
                            reason2w = thn[reason2]
                    if userweights[user1] == userweights[user2]:
                        if reason1w >= reason2w:
                            value = 0
                        elif reason2w > reason1w:
                            value = 1
                    elif userweights[user1] < userweights[user2]:
                        value = 1
                    else:
                        value = 0
                    if reason1 == "health" and reason2 != "health" and reason2 != "security":
                        value = 1
                    elif reason1 != "health" and reason2 == "health" and reason1 != "security":
                        value = 0
                    elif (reason1 == "health" and reason2 == "security") or (
                                    reason2 == "health" and reason1 == "security"):
                        value = 1
                    n = random.random()
                    str1 = str(k) + divider + user1 + divider + user2 + divider + reason1 + divider + reason2 + divider
                    str1 = start + str1 + str(value) + "');"
                    if n < 0.80:
                        cur.execute(str1)
                        con.commit()
                        k = k + 1
                    m = m + 1

                    print(m)

cur.execute('SELECT * FROM `cases`')
print(cur.fetchall())
cur.close()
con.close()
