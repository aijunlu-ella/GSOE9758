import json
import requests
import time

token = "A1E-NwVOSObFDOwUcRtljla294Q8U3ir5t"

"""
Get values from variable 
"""
def get_values_ubidots(device_label, var_label, items):

    base_url = "http://things.ubidots.com/api/v1.6/devices/" + device_label + "/" + var_label + "/values"
    try:
        r = requests.get(base_url + '?token=' + token + "&page_size=" + str(items), timeout=20)
        return r.json()
    except Exception as e:
        print(e)
        return {'error':'Request failed or timed out'}

"""
Main function
"""
if __name__ == '__main__':

    device_label = "yun"
    var_label = "avg-weight"
    values_weight = get_values_ubidots(device_label, var_label, 10)
    retrive_weight_time = values_weight['results'][0]['timestamp']
    retrive_weight_value = values_weight['results'][0]['value']
    print(retrive_weight_time,retrive_weight_value)
##    print(type(retrive_weight_time),type(retrive_weight_value))
    var_label = "position"
    values_position = get_values_ubidots(device_label, var_label, 10)
    retrive_position_time = values_position['results'][0]['timestamp']
    retrive_position_value = values_position['results'][0]['value']
    if int(retrive_position_value):
        retrive_position_lat = float(values_position['results'][0]['context']['lat'])
        retrive_position_lng = float(values_position['results'][0]['context']['lng'])
        print(retrive_position_time,retrive_position_lat,retrive_position_lng)
