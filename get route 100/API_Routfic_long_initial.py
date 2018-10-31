##written by z5196135
##using 98 random locations in sampledata csv to generate an optimal route by routific apis and store it into route.csv 
import urllib.request
import json
import csv
import os
import time




URL   = "https://api.routific.com/v1/vrp-long"

URL2 = "https://api.routific.com/jobs/"



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
          "capacity": 200,
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
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1YmI5NzFmZDdjN2MzYzFiZTI2OGMxNDIiLCJpYXQiOjE1Mzg4Nzk5OTd9.myeEHT1p4p41uaHR-2f_U8PHg1erqvnkjZ0Sj5YAwXk'

    req = urllib.request.Request(URL, json.dumps(data).encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', "bearer " + token)

    # Step 6: Get route
    res = urllib.request.urlopen(req).read()
    solutions = json.loads(res)
    job_id = solutions["job_id"]

    time.sleep(10)


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
filename = 'sample data.csv'
order = get_orders(filename)
order.pop(0)

routefile = 'route.csv'
if not os.path.exists(routefile):
    with open(routefile,"a+") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["name","lat","lng","start","end","load","priority"])

for i in range(len(order)):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for name,lat,lng,start,end,load,priority in reader:
            if name == order[i][1]:
                with open(routefile,"a+") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([name,lat,lng,start,end,load,priority])
print('Stored the route data into route.csv')

