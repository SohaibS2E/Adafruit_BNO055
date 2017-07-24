#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

#define BNO055_SAMPLERATE_DELAY_MS (33)          // Delay between data requests

Adafruit_BNO055 bno = Adafruit_BNO055();          // Create sensor object bno based on Adafruit_BNO055 library

void setup(void)
{
  Serial.begin(115200);                           // Begin serial port communication
  if(!bno.begin())                                // Initialize sensor communication
  {  
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");  
  }
  delay(1000);
  bno.setExtCrystalUse(true);                     // Use the crystal on the development board
}

void loop(void)
{
  String imuData;
  imu::Quaternion quat = bno.getQuat();
  imu::Vector<3> euler = bno.getVector(Adafruit_BNO055::VECTOR_EULER);

  imuData+= String(quat.w()) +","; 
  imuData+=String(quat.x())+",";  
  imuData+=String(quat.y()) + ",";  
  imuData+=String(quat.z())+",";
  imuData+=String(euler.x())+",";
  imuData+=String(euler.y())+",";
  imuData+=String(euler.z());
  Serial.println(imuData);
  delay(BNO055_SAMPLERATE_DELAY_MS);              // Pause before capturing new data
}

