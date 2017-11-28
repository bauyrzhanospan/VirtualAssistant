import urllib.request


def change_politics():
    Temp = open("./Conf/temp_politics.conf", "r")
    Global = open("./Conf/politics.conf", "r")
    tempo = Temp.readlines()
    Globaly = Global.readlines()
    DF = [x for x in tempo if x not in Globaly]
    Temp.close()
    Global.close()
    Temp = "./Conf/temp_politics.conf"
    Global = "./Conf/politics.conf"
    for line in DF:
        data = line.split(":")
        if str(data[4]) != "temp\n":
            with open(Global, "a") as word_file:
                word_file.write(str(line))
    with open(Temp, "w") as f:
        with open(Global, "r") as d:
            for line in d:
                f.write(str(line))
    return 0


def check_same(order):
    data = urllib.request.urlopen("http://10.12.102.156/port_3480/data_request?id=lu_status").read()
    d = data.decode("utf-8")
    if order == "KettleOff":
        device = 19
        status = 0
        Status = int(d.split('"id": ' + str(device))[1].split('" }', 1)[0].strip()[-1])
        if Status == status:
            return 1
        else:
            return 0
    elif order == "KettleOn":
        device = 19
        status = 1
        Status = int(d.split('"id": ' + str(device))[1].split('" }', 1)[0].strip()[-1])
        if Status == status:
            return 1
        else:
            return 0
    elif order == "LampOn":
        device = 395
        status = 1
        Status = int(d.split('"id": ' + str(device))[1].split('" }', 1)[0].strip()[-1])
        if Status == status:
            return 1
        else:
            return 0
    elif order == "LampOff":
        device = 395
        status = 0
        Status = int(d.split('"id": ' + str(device))[1].split('" }', 1)[0].strip()[-1])
        if Status == status:
            return 1
        else:
            return 0

