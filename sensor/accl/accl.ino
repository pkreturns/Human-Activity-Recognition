#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 mpu;

void setup() {
  Serial.begin(9600);
  
  Wire.begin();
  
  if (!mpu.begin()) {
    Serial.println("Failed to initialize MPU-6050");
    while (1);
  }
  
  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
}

void loop() {
  sensors_vec_t accelerometer;
  mpu.getEvent(&accelerometer);

  float accelX = accelerometer.x;
  float accelY = accelerometer.y;
  float accelZ = accelerometer.z;

  Serial.print("Accel X: ");
  Serial.print(accelX);
  Serial.print(", Accel Y: ");
  Serial.print(accelY);
  Serial.print(", Accel Z: ");
  Serial.println(accelZ);

  delay(1000);  // Adjust delay as needed
}
