import urllib.request
from datetime import datetime, time, timedelta


def in_between(now, start, end):
    if start <= end:
        return start <= now < end
    else:  # over midnight e.g., 23:30-04:15
        return start <= now or now < end


def check_pol(order, username, reason):
    conf_file = "./Conf/temp_politics.conf"
    politics = []
    pol = dict.fromkeys(["start", "stop", "users", "device", "preference", "status"])

    now = datetime.now()
    now_time = now.time()
    noway = []
    bush = []

    if order[-1:] == "f":
        act = "On"
    else:
        act = "Off"
    if order[0] == "K":
        dev = "19"
    else:
        dev = "395"
    for element in politics:
        startHour = int(str(element["start"])[:-2])
        startMin = int(str(element["start"])[-2:])
        stopHour = int(str(element["stop"])[:-2])
        stopMin = int(str(element["stop"])[-2:])
        if in_between(now_time, time(startHour, startMin), time(stopHour, stopMin)) and act == str(
                element["status"]) and dev == str(element["device"]):
            if compare_user(username, find_high(element)) == 0:
                return 9
            noway.append(politics.index(element))
    if not noway:
        return 0
    else:
        for el in noway:
            bush.append(politics[el])
        if reason == 0:
            return 1
        else:
            for el in bush:
                if compare(el["preference"], reason, username) == 1:
                    return 1
                elif compare(el["preference"], reason, username) == 0:
                    return 3
                else:
                    return 0
