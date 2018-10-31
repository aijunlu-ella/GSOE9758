##written by z5196135
##This is a version without uesr interface
import urllib.request
import json
import csv
import os
import time
import math
import requests
from datetime import datetime



URL   = "https://api.routific.com/v1/vrp-long"

URL2 = "https://api.routific.com/jobs/"

token = "#####your token from ubidots##########"

def frange(start,stop, step=1.0):
    while start < stop:
        yield start
        start +=step

def get_values_ubidots(device_label, var_label, items):

    base_url = "http://things.ubidots.com/api/v1.6/devices/" + device_label + "/" + var_label + "/values"
    try:
        r = requests.get(base_url + '?token=' + token + "&page_size=" + str(items), timeout=20)
        return r.json()
    except Exception as e:
        print(e)
        return {'error':'Request failed or timed out'}

def post_values(device_label, var_label, items):

    base_url = "http://things.ubidots.com/api/v1.6/devices/" + device_label + "/" + var_label + "/values"
    try:
        r = requests.post(base_url + '?token=' + token, json=items)
        return r.json()
    except Exception as e:
        print(e)
        return {'error':'Request failed or timed out'}
    

# Step 2: Prepare visits
def get_orders(filename):
    def check_process():
        job_status_request = URL2 + job_id
        job_status_j = urllib.request.urlopen(job_status_request).read()
        job_status = json.loads(job_status_j)
        return job_status
    visits={}
    if not os.path.exists(filename):
        print(f'There is no file named {filename} in the working directory, giving up...')
        sys.exit()
    with open(filename) as file:
        has_header = csv.Sniffer().has_header(file.read(1024))
        file.seek(0)
        csv_file = csv.reader(file)
        if has_header:
            next(csv_file)
        count = 1
        for name,lat,lng,start,end,load,priority in csv_file:
            order = 'order_{}'.format(count)
            visits[order]={"location":{"name":name,"lat":float(lat),"lng":float(lng)}}
            if start:
                visits[order]['start'] = start
            if end:
                visits[order]['end'] = end
            if load:
                visits[order]['load'] = int(load)
            if priority:
                visits[order]['priority'] = priority
            count+=1
      

    # Step 3: Prepare vehicles
    fleet = {
        "vehicle_1": {
          "start_location": {
            "id": "depot",
            "name": "Sydney NSW 2052, Australia",
            "lat": -33.917347,
            "lng": 151.231268
          },
          "end_location": {
            "id": "depot",
            "name": "Sydney NSW 2052, Australia",
            "lat": -33.917347,
            "lng": 151.231268
          },
          "shift_start": "6:00",
          "shift_end": "15:00",
          "capacity": 100,
        },
       
    }

    # Step 4: Prepare data payload
    data = {
        "visits": visits,
        "fleet": fleet
    }
    ##print(data)

    ##Step 5: Put together request
    # This is your demo token
    token = "#####your token from routific##########"

    req = urllib.request.Request(URL, json.dumps(data).encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', "bearer " + token)

    # Step 6: Get route
    res = urllib.request.urlopen(req).read()
    solutions = json.loads(res)
    job_id = solutions["job_id"]


    job_status=check_process()
    print(job_status['status'])
    while job_status['status']!='finished':
        time.sleep(5)
        job_status=check_process()
        print(job_status['status'])
        
    ##
    order_of_route = []
    for i in range (count):
        order_of_route.append((job_status["output"]['solution']['vehicle_1'][i]['location_id'],
                               job_status["output"]['solution']['vehicle_1'][i]['location_name'],
                             ))
    return(order_of_route)

print('getting deliver orders......')
filename = 'one location.csv'
order = get_orders(filename)
order.pop(0)

error_log = "error log.csv"
if not os.path.exists(error_log):
    with open(error_log,"a+") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["time","name","lat","lng","current_lat","current_lng","load","current_load"])


for i in range(len(order)):
    print(f'{i}:{order[i][0]}  order_name---{order[i][1]}')
while len(order):
    flag = 0
    orderstatus = input('Have you finished this order? Yes/No').strip().lower()
    while flag < 3:
        if orderstatus[0]=='y':
            device_label = "yun"
            var_label = "avg-weight"
            error_reply = {'error':'Request failed or timed out'}
            values_weight = get_values_ubidots(device_label, var_label, 100)
##            print(values_weight)
            while values_weight == error_reply:
                values_weight = get_values_ubidots(device_label, var_label, 100)
##                print(values_weight)
            retrive_weight_time = values_weight['results'][0]['timestamp']//1000
            retrive_weight_value = abs(float(values_weight['results'][0]['value']))
##            print(retrive_weight_time,retrive_weight_value)
        ##    print(type(retrive_weight_time),type(retrive_weight_value))
            var_label = "position"
            values_position = get_values_ubidots(device_label, var_label, 100)
##            print(values_position)
            while values_position == error_reply:
                values_position = get_values_ubidots(device_label, var_label, 100)
##                print(values_position)
            retrive_position_value = int(values_position['results'][0]['value'])
            while not retrive_position_value:
                values_position = get_values_ubidots(device_label, var_label, 100)
            retrive_position_time = values_position['results'][0]['timestamp']//1000
            retrive_position_lat = float(values_position['results'][0]['context']['lat'])
            retrive_position_lng = float(values_position['results'][0]['context']['lng'])
##            print(retrive_position_time,retrive_position_lat,retrive_position_lng)
            with open(filename) as csvfile:
                reader = csv.reader(csvfile)
                for name,lat,lng,start,end,load,priority in reader:
                    if name == order[0][1]:
                        lat_order = float(lat)
                        lng_order = float(lng)
                        load_order = float(load)
                        if retrive_position_time in range (int(time.time())-172060,int(time.time())):
                            lat_diff = int(abs(retrive_position_lat-lat_order)*1000)
                            lng_diff = int(abs(retrive_position_lng-lng_order)*1000)
                            load_diff = int(abs(retrive_weight_value-load_order))
                            if not lat_diff:
                                if not lat_diff:
                                    print('location matched')
                                    if not load_diff:
                                        print('load matched')
                                        order.pop(0)
                                        finish_order = 1
                                    else:
                                        print('check item')
                                        flag += 1
                                        
                            else:
                                print("check location")
                                flag += 1
##write errorlog to ubidots
    values = 0
    device_label = "yun"
    var_label = "error-log"
    payload = [{'value':1,'timestamp':values_position['results'][0]['timestamp'],'context':{"location":(lat_order,lng_order),'current_location':(retrive_position_lat,retrive_position_lng),\
                                                            "load":load_order,"current load":retrive_weight_value}}]
    while not values:
        values = post_values(device_label, var_label, payload)
##write errorlog in local
    with open(error_log,"a+") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([datetime.utcfromtimestamp(retrive_position_time).strftime('%Y-%m-%d %H:%M:%S'),order[0][1],lat_order,lng_order,retrive_position_lat,retrive_position_lng,load_order,retrive_weight_value])
    order.pop(0)
    print('error occur')
    continue

print('finish all the task')
    

