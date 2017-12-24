#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import RBR
from CBR import CBR
import Classification as classify
import urllib
import re


# This function changes status of the device by sending post request to the Vera
# Then it generates answer, forex: "Lamp is turned on" for order "LampOn"
# As an input there is order type (defined, not raw)
def Give_answer(order):
    # If order is "KettleOff"
    if order == "KettleOff":
        # Send POST request to Vera
        url = "http://10.12.102.156/port_3480/data_request?id=lu_action&output_format=json&DeviceNum=19&serviceId=urn" \
              ":upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue=0&rand=0.9835083063374366 "
        urllib.request.urlopen(url)
        # Return the answer
        return "Kettle is turned off"
    # The same for others
    elif order == "KettleOn":
        url = "http://10.12.102.156/port_3480/data_request?id=lu_action&output_format=json&DeviceNum=19&serviceId=urn" \
              ":upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue=1&rand=0.8954535030571291 "
        urllib.request.urlopen(url)
        return "Kettle is turned on"
    elif order == "LampOn":
        url = "http://10.12.102.156/port_3480/data_request?id=lu_action&output_format=json&DeviceNum=395&serviceId" \
              "=urn:upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue=1 "
        urllib.request.urlopen(url)
        return "Lamp is turned on"
    elif order == "LampOff":
        url = "http://10.12.102.156/port_3480/data_request?id=lu_action&output_format=json&DeviceNum=395&serviceId" \
              "=urn:upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue=0&rand=0.46221056753903733 "
        urllib.request.urlopen(url)
        return "Lamp is turned off"


# Dialogue Manager part for order classification and giving answer
# As an input it takes raw order and username
def DMorder(text, username):
    # text is raw input
    # It classifies order by classification module
    # outputs of the RBR function are:
    # 0 - device in the same status
    # 1 - there is conflict!
    # 2 - device is changed - it is ok
    order = classify.classifyO(text)

    # It takes response from Rule-Based Reasoner
    # outputs of the function DMorder:
    # 0 - yes or no?
    # 1 - device is already in the status you need OR device changed
    resp, conflict = RBR.RBR(order, username)
    responce = 1
    answer = ""

    # If response is 0, then -> device is in the status that user need
    if resp == 0:
        responce = 1
        answer = "Device is already in status you need."
    # If response is 2, then -> there is no conflict, so change device status
    elif resp == 2:
        responce = 1
        answer = Give_answer(order)
    # If response is 1, then -> there is a conflict
    # Send data about it and render response page
    elif resp == 1:
        responce = 0
        answer = "Sorry, another user (" + str(conflict["user"]) + \
                 ") has already set the device in an opposite status." \
                 " Do you want to try to change it anyway? Answer yes or no: "

    # conflict - conflicting rule full data
    return responce, answer, conflict, order


# Dialogue Manager to reason classification
# Function takes raw reason, username and order as an input
def DMreason(text, username, order):
    # conflict - conflicting rule full data as a dictionary, conflict["user"] = usertype
    # Classification of reason
    reason = classify.classifyR(text)
    # We need to know user type
    usertypein = RBR.Usertype(username)
    # Import rules from database
    rules = RBR.importrules()
    order2 = order
    # Classification of order
    orderDevice = re.sub('[On]', '', order2)
    orderDevice = re.sub('[Off]', '', orderDevice)
    if order[-1] == "n":
        orderStatus = 0
    else:
        orderStatus = 1
    orderdata = [orderDevice, orderStatus]
    # Check conflict
    conflict = RBR.checkTime(orderdata, rules)
    while conflict == None:
        conflict = RBR.checkTime(orderdata, rules)
    # Create variables to input to CBR
    usertypeout = conflict["user"]
    reasonout = conflict["reason"]
    # Take response form CBR and answer to user by returning answer, emoji type and other data
    responce = CBR.main(usertypein, usertypeout, reason, reasonout)
    if responce == 0:
        answer = "Sorry, your reason is not strong enough"
        smile = "https://github.com/BiggyBaron/VirtualAssistant/blob/master/static/sorry.gif?raw=true"
    else:
        answer = Give_answer(order)
        smile = "https://github.com/BiggyBaron/VirtualAssistant/blob/master/static/sucsses.gif?raw=true"
    return answer, reason, smile, responce
