#include "robolib.h"
#include "Dynamixel.h"

RobotControl::RobotControl(int bType, int bRate): Dynamixel(bType)
{
  boardType = bType;
  baudRate = bRate;
  Dynamixel::begin(baudRate);
}

void RobotControl::torqueOnOff(uint8 ID, int setting){
  int address = 24;
  Dynamixel::writeWord(ID, address, setting);
}

void RobotControl::setLocation(uint8 ID, int location){
  int address = 30;
  Dynamixel::writeWord(ID, address, location);
}

void RobotControl::setSpeed(uint8 ID, int speed){
  int address = 32;
  Dynamixel::writeWord(ID, address, speed);
}

void RobotControl::setTorque(uint8 ID, int speed){
  int address = 34;
  Dynamixel::writeWord(ID, address, speed);
}

int RobotControl::readLocation(uint8 ID)
{
  int location;
  int hAddress = 37;
  int lAddress = 36;
  int hByte = Dynamixel::readByte(ID, hAddress);
  int lByte = Dynamixel::readByte(ID, lAddress);
  hByte = hByte << 8;
  location = hByte | lByte;
  return location;
}

int RobotControl::readTorque(uint8 ID)
{
  int torque;
  int hAddress = 41;
  int lAddress = 40;
  int hByte = Dynamixel::readByte(ID, hAddress);
  int lByte = Dynamixel::readByte(ID, lAddress);
  hByte = hByte << 8;
  torque = hByte | lByte;
  return torque;
}

int RobotControl::readSpeed(uint8 ID)
{
  int speed;
  int hAddress = 39;
  int lAddress = 38;
  int hByte = Dynamixel::readByte(ID, hAddress);
  int lByte = Dynamixel::readByte(ID, lAddress);
  hByte = hByte << 8;
  speed = hByte | lByte;
  return speed;
}




