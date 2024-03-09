#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

const char* ssid     = "ZTE-tAf9NA";
const char* password = "pykg793q";
String apiKeyValue = "tPmAT5Ab3j7F9";


String sensorName = "Activity Recognition";
String sensorLocation = "Angamaly";

#define ON_Board_LED 2 //Blue LED
#include <Wire.h> //library allows communication with I2C / TWI devices
#include <math.h> //library includes mathematical functions


#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 mpu;

const int MPU=0x68; //I2C address of the MPU-6050
int16_t AcX,AcY,AcZ;
void setup()
{ 
    mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
    Wire.begin(); //initiate wire library and I2C
    Wire.beginTransmission(MPU); //begin transmission to I2C slave device
    Wire.write(0x6B); // PWR_MGMT_1 register
    Wire.write(0); // set to zero (wakes up the MPU-6050)  
    Wire.endTransmission(true); //ends transmission to I2C slave device
    Serial.begin(9600); //serial communication at 9600 bauds

    WiFi.begin(ssid, password);
    Serial.println("Connecting");

    while(WiFi.status() != WL_CONNECTED) { 
    delay(500);
    Serial.print(".");

    }
    Serial.print("Connected to WiFi network with IP Address: ");
    Serial.println(WiFi.localIP());
    delay(100);
}

void loop()
{
    Wire.beginTransmission(MPU); //begin transmission to I2C slave device
    Wire.write(0x3B); // starting with register 0x3B (ACCEL_XOUT_H)
    Wire.endTransmission(false); //restarts transmission to I2C slave device
    Wire.requestFrom(MPU,14,true); //request 14 registers in total  

    //read accelerometer data
    AcX=Wire.read()<<8|Wire.read(); // 0x3B (ACCEL_XOUT_H) 0x3C (ACCEL_XOUT_L)  
    AcY=Wire.read()<<8|Wire.read(); // 0x3D (ACCEL_YOUT_H) 0x3E (ACCEL_YOUT_L) 
    AcZ=Wire.read()<<8|Wire.read(); // 0x3F (ACCEL_ZOUT_H) 0x40 (ACCEL_ZOUT_L)
    float x=(float)AcX/16384;
    float y=(float)AcY/16384;
    float z=(float)AcZ/16384;
     
    x=x-0.39;
    y=y-0.01;
    z=z-0.02;
    x=x*64;
    y=y*64;
    z=z*64;
    Serial.print("Accelerometer: ");
    Serial.print("X = "); Serial.print(x);
    Serial.print(" Y = "); Serial.print(y);
    Serial.print(" Z = "); Serial.println(z); 
  
//    delay(1000);

    if(WiFi.status()== WL_CONNECTED ){

      digitalWrite(ON_Board_LED, LOW);//wifi connected LED on
    
      HTTPClient http; 
      http.begin("http://192.168.1.73/activity/post-esp-data.php");//max:192.168.43.39//Nandanam:192.168.1.73//Moskov:192.168.1.22
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");  
      String httpRequestData = "api_key=" + apiKeyValue + "&sensor=" + sensorName+ "&location=" + sensorLocation + "&value1=" + x+ "&value2=" + y +"&value3=" + z + "";
      Serial.print("Upload_Data: ");
      Serial.println(httpRequestData); 
      int httpResponseCode = http.POST(httpRequestData);
      Serial.print("Upload_ResponseCode: ");
      Serial.println(httpResponseCode); 
      delay(32);
          
     }

      else {
             //Serial.println("WiFi Disconnected");
             digitalWrite(ON_Board_LED, HIGH);//wifi connected LED on
           }

}
