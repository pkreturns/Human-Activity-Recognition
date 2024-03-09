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
    
    Serial.print("Accelerometer: ");
    Serial.print("X = "); Serial.print(x*64);
    Serial.print(" Y = "); Serial.print(y*64);
    Serial.print(" Z = "); Serial.println(z*64); 
  
    delay(1000);
}
