##written by z5196135
##get route info from google
import urllib.request
import json

endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
api_key = 'AIzaSyDQiWUJhriaJNxeKJ97X7wS7mp7dCUDtKQ'
origin = input('Where are you? ').replace(' ','+')
destination = input('Where do you want to go?').replace(' ','+')

nav_request = 'origin={}&destination={}&key={}&mode=driving'.format(origin,destination,api_key)
request = endpoint + nav_request
response = urllib.request.urlopen(request).read()
directions = json.loads(response)
total_distance = directions['routes'][0]['legs'][0]['distance']['text']
print(f'total_distance:',total_distance)
total_time = directions['routes'][0]['legs'][0]['duration']['text']
print(f'total_time:',total_time)
steps = directions['routes'][0]['legs'][0]['steps']
for i in range(len(steps)):
    print(f'STEP{i+1} is:')
    print(steps[i]['html_instructions'][0:4]+' '+steps[i]['html_instructions'][8:12]+'at '+str(steps[i]['end_location']))


