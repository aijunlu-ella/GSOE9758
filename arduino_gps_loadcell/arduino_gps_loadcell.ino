//

#include <UbidotsYUN.h>
#include <SoftwareSerial.h>
#include <TinyGPS++.h>
#include <HX711_ADC.h>
#include <math.h> 

/****************************************
 * Define Constants
 ****************************************/
#define TOKEN //####################################### your ubidots token
#define VARIABLE_LABEL "position"  // Change for your variable label desired


Ubidots client(TOKEN);

TinyGPSPlus gps;
SoftwareSerial serial_connection(10,11); //for gps RX=PIN10,TX=PIN11
HX711_ADC LoadCell(3, 4);
long t;
float l;
void setup() {
  client.init();
  Serial.begin(9600);
  serial_connection.begin(9600);
  Serial.println("GPS START");
  // put your setup code here, to run once:
  Serial.println("Wait...");
  LoadCell.begin();
  long stabilisingtime = 180000; // tare preciscion can be improved by adding a few seconds of stabilising time and gps also need 3 minutes start up time
  LoadCell.start(stabilisingtime);
  LoadCell.setCalFactor(696.0); // user set calibration factor (float)
  Serial.println("Startup + tare is complete");

}

void loop() {
  // put your main code here, to run repeatedly:
  while(serial_connection.available())
  {
    gps.encode(serial_connection.read());
    }
    if (gps.location.isUpdated())
    {
      //read gps data
      Serial.println("Satellite Count:");
      Serial.println(gps.satellites.value());
      Serial.println("lat:");
      Serial.println(gps.location.lat());
      Serial.println("lng:");
      Serial.println(gps.location.lng());
      Serial.println("speed mph:");
      Serial.println(gps.speed.mph());
      Serial.println("Altitude Feet:");
      Serial.println(gps.altitude.feet());
      Serial.println("");
      char lati[15];
      char longt[15];
      char context[50];
      float value1 = analogRead(A0);
      dtostrf(gps.location.lat(), 9, 7, lati);
      dtostrf(gps.location.lng(), 9, 7, longt);
      Serial.println(lati);
      sprintf(context, "\"lat\"=%s$\"lng\"=%s", lati, longt); //Sends latitude and longitude for watching position in a map
      Serial.println(context);
      client.add(VARIABLE_LABEL,1,context);   // add gps data to the content to add to ubidots
      LoadCell.update();
      //get smoothed value from data set + current calibration factor
      if (millis() > t + 1000) {
        float i = LoadCell.getData();
        float v = LoadCell.getCalFactor();
        Serial.print("Load_cell output val: ");
        Serial.print(i);
        Serial.print("      Load_cell calFactor: ");
        Serial.println(v);
        t = millis();
        client.add("weight",v);//add weight data to the content to add to ubidots
      }
      //receive from serial terminal
      if (Serial.available() > 0) {
        float i;
        char inByte = Serial.read();
        if (inByte == 'l') i = -1.0;
        else if (inByte == 'L') i = -10.0;
        else if (inByte == 'h') i = 1.0;
        else if (inByte == 'H') i = 10.0;
        else if (inByte == 't') LoadCell.tareNoDelay();
        if (i != 't') {
          float v = LoadCell.getCalFactor() + i;
          LoadCell.setCalFactor(v);
        }
      }
      //check if last tare operation is complete
      if (LoadCell.getTareStatus() == true) {
        Serial.println("Tare complete");
      }
      delay(1000);
      client.sendAll();//send data to ubidots
      }
}
