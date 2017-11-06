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


def check_device():
    # TODO: make this in Lab
    print("")
