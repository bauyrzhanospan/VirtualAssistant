def Give_answer(order):
    now = datetime.now()
    clock = str(now.time())
    if order == "KettleOff":
        device = "19"
        status = "Off"
        url = "http://10.12.102.156/port_3480/data_request?id=lu_action&output_format=json&DeviceNum=19&serviceId=urn" \
              ":upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue=0&rand=0.9835083063374366 "
        urllib.request.urlopen(url)
        return "Kettle is turned off for " + str(10) + " minutes"
    elif order == "KettleOn":
        device = "19"
        status = "On"
        url = "http://10.12.102.156/port_3480/data_request?id=lu_action&output_format=json&DeviceNum=19&serviceId=urn" \
              ":upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue=1&rand=0.8954535030571291 "
        urllib.request.urlopen(url)
        return "Kettle is turned on for " + str(10) + " minutes"
    elif order == "LampOn":
        device = "395"
        status = "On"
        url = "http://10.12.102.156/port_3480/data_request?id=lu_action&output_format=json&DeviceNum=395&serviceId" \
              "=urn:upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue=1 "
        urllib.request.urlopen(url)
        return "Lamp is turned on for " + str(10) + " minutes"
    elif order == "LampOff":
        device = "395"
        status = "Off"
        url = "http://10.12.102.156/port_3480/data_request?id=lu_action&output_format=json&DeviceNum=395&serviceId" \
              "=urn:upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue=0&rand=0.46221056753903733 "
        urllib.request.urlopen(url)
        return "Lamp is turned off for " + str(10) + " minutes"