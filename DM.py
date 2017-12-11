import RBR
from CBR import CBR
import Classification as classify
from datetime import datetime
import urllib
import re

def Give_answer(order):
    now = datetime.now()
    clock = str(now.time())
    if order == "KettleOff":
        device = "19"
        status = "Off"
        url = "http://10.12.102.156/port_3480/data_request?id=lu_action&output_format=json&DeviceNum=19&serviceId=urn" \
              ":upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue=0&rand=0.9835083063374366 "
        urllib.request.urlopen(url)
        return "Kettle is turned off"
    elif order == "KettleOn":
        device = "19"
        status = "On"
        url = "http://10.12.102.156/port_3480/data_request?id=lu_action&output_format=json&DeviceNum=19&serviceId=urn" \
              ":upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue=1&rand=0.8954535030571291 "
        urllib.request.urlopen(url)
        return "Kettle is turned on"
    elif order == "LampOn":
        device = "395"
        status = "On"
        url = "http://10.12.102.156/port_3480/data_request?id=lu_action&output_format=json&DeviceNum=395&serviceId" \
              "=urn:upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue=1 "
        urllib.request.urlopen(url)
        return "Lamp is turned on"
    elif order == "LampOff":
        device = "395"
        status = "Off"
        url = "http://10.12.102.156/port_3480/data_request?id=lu_action&output_format=json&DeviceNum=395&serviceId" \
              "=urn:upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue=0&rand=0.46221056753903733 "
        urllib.request.urlopen(url)
        return "Lamp is turned off"


def DMorder(text, username):
    # text is raw input
    order = classify.classifyO(text)
    # outputs of the RBR function are:
    # 0 - device in the same status
    # 1 - there is conflict!
    # 2 - device is changed - it is ok

    resp, conflict = RBR.RBR(order, username)
    responce = 1
    answer = ""

    # outputs of the function DMorder:
    # 0 - yes or no?
    # 1 - device is already in the status you need OR device changed
    if resp == 0:
        responce = 1
        answer = "Device is already in status you need."
    elif resp == 2:
        responce = 1
        answer = Give_answer(order)
    elif resp == 1:
        responce = 0
        answer = "Sorry, another user (" + str(conflict["user"]) + \
                 ") has already set the device in an opposite status." \
                 " Do you want to try to change it anyway? Answer yes or no: "

    return responce, answer, conflict, order
    # conflict - conflicting rule full data


def DMreason(text, username, order):
    # conflict - conflicting rule full data as dictionary, conflict["user"] = usertype
    print(order)
    reason = classify.classifyR(text)
    usertypein = RBR.Usertype(username)
    rules = RBR.importrules()
    print("Here is conflict")
    order2 = order
    orderDevice = re.sub('[On]', '', order2)
    orderDevice = re.sub('[Off]', '', orderDevice)
    if order[-1] == "n":
        orderStatus = 0
    else:
        orderStatus = 1
    orderdata = [orderDevice, orderStatus]
    print(orderdata)
    print(rules)
    conflict = RBR.checkTime(orderdata, rules)
    print(conflict)
    while conflict == None:
        conflict = RBR.checkTime(orderdata, rules)
    usertypeout = conflict["user"]
    reasonout = conflict["reason"]

    responce = CBR.main(usertypein, usertypeout, reason, reasonout)
    if responce == 0:
        answer = "Sorry, your reason is not strong enough"
        smile = "https://github.com/BiggyBaron/VirtualAssistant/blob/master/static/sorry.gif?raw=true"
    else:
        answer = Give_answer(order)
        smile = "https://github.com/BiggyBaron/VirtualAssistant/blob/master/static/sucsses.gif?raw=true"
    return answer, reason, smile, responce
