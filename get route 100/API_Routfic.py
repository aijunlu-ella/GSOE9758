# Step 1: Import http client and set routific vrp url
import urllib.request
import json

URL   = "https://api.routific.com/v1/vrp"

# Step 2: Prepare visits
visits = {
    "order_1": {
      "location": {
        "name": "Camperdown NSW 2006, Australia",
        "lat": -33.888584,
        "lng": 151.187347
      }
    },
    "order_2": {
      "location": {
        "name": "891 Elizabeth St, Waterloo NSW 2017, Australia",
        "lat": -33.902605,
        "lng": 151.205578
      }
    },
    "order_3": {
      "location": {
        "name": "6 Coward St, Rosebery NSW 2018, Australia",
        "lat": -33.9267,
        "lng": 151.205668
      }
    },
        "order_4": {
      "location": {
        "name": "1 Bay St, Glebe NSW 2037, Australia",
        "lat": -33.882942,
        "lng": 151.194119
      }
    },
        "order_5": {
      "location": {
        "name": "10 McEvoy St, Waterloo NSW 2017, Australia",
        "lat": -33.900824,
        "lng": 151.208008
      }
    },
}

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
      }
    },
   
}

# Step 4: Prepare data payload
data = {
    "visits": visits,
    "fleet": fleet
}

print(data)

### Step 5: Put together request
### This is your demo token
##token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1YmI5NzFmZDdjN2MzYzFiZTI2OGMxNDIiLCJpYXQiOjE1Mzg4Nzk5OTd9.myeEHT1p4p41uaHR-2f_U8PHg1erqvnkjZ0Sj5YAwXk'
##
##req = urllib.request.Request(URL, json.dumps(data).encode('utf-8'))
##req.add_header('Content-Type', 'application/json')
##req.add_header('Authorization', "bearer " + token)
##
### Step 6: Get route
##res = urllib.request.urlopen(req).read()
##solutions = json.loads(res)
##for i in range(len(solutions['solution']['vehicle_1'])):
##    print (solutions['solution']['vehicle_1'][i])
##
