import urllib.request
import json
import csv
import sys
import os

def isfloat(n):
    try:
        float(n)
        return True
    except ValueError:
        return False

endpoint = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
api_key = 'AIzaSyDQiWUJhriaJNxeKJ97X7wS7mp7dCUDtKQ'
lat = input('lat ').replace(' ','+')
lng = input('lng ').replace(' ','+')
filename = input('What is your csv file name')+'.csv'
if not os.path.exists(filename):
    with open(filename,"a+") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["name","lat","lng","url"])

if isfloat(lat) and isfloat(lng):
    location = 'location={},{}'.format(lat,lng)
    nav_request = '&radius=1000&types=food&name=cafe&key={}'.format(api_key)
    request = endpoint + location + nav_request
    response = urllib.request.urlopen(request).read()
    places = json.loads(response)




    with open(filename,"a+") as csvfile:
        writer = csv.writer(csvfile)
        for i in range(len(places['results'])):
            L=[]
            L.append(places['results'][i]['name'])
            L.append(places['results'][i]['geometry']['location']['lat'])
            L.append(places['results'][i]['geometry']['location']['lng'])
            writer.writerow(L)
else:
    print("Input error!")
    sys.exit()
