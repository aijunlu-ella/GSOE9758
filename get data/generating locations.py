import csv
import os


visits={}
filename = input('What is your csv file name')+'.csv'
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
    for name,lat,lng in csv_file:
        order = 'order_{}'.format(count)
        visits[order]={"location":{"name":name,"lat":float(lat),"lng":float(lng)}}
        count+=1
print(visits)
        
        
    
