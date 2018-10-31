# GSOE9758

# arduino_gps_loadcell.ino
The main function of this code is to collect GPS and weight data from Arduino Yun and send them to Ubidots after getting GPS module initialized and load cell tared.

# API_Routfic_long_initial.py
We get the csv from database(sampledata.csv) and convert it into payload written in json. By using the Routific APIs, we can get the optimal route for 100 destinations within 2 minutes.
Please input your own api key.
You can compare before and after in sampledata.csv and route.csv

# widget.py
The main function of the code is to check whether goods have been delivered to the right location and provide a user interface for the driver. Also, optimal route planner is included in the code.
Please input your own api key.
You can find out the results in route.csv, success.csv, errorlog.csv and the 1024.avi shows the whole process of the sample test.

For other files in the directory, please check the header of the file for details.
