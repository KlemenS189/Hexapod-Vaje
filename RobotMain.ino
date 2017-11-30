#include <robolib.h>
#define interval 1000

//Spremenljivke
int bufer[9];
int a,b,c,d,e,f,g,h,i,j;
int kot1,kot2,kot3,kot4;
int navor1,navor2,navor3,navor4;
int ID;
int navor;
int hitrost;
int zacetek=0;
int konec;
int temp;
int imeCheckNavor=0;

//Objekti
RobotControl cmd(3,1);

//Funckije
void torqueSend();

//Dynamixel Dxl(3);
void setup() {
  //Dxl.begin(1);
  SerialUSB.begin();
  cmd.setSpeed(1, 100);
  cmd.setSpeed(2, 100);
  cmd.setSpeed(3, 100);
  cmd.setSpeed(4, 100);

  cmd.setLocation(1, 512);
  cmd.setLocation(2, 300);
  cmd.setLocation(3, 300);
  cmd.setLocation(4, 500);

  cmd.setSpeed(1, 100);
  cmd.setSpeed(2, 100);
  cmd.setSpeed(3, 100);
  cmd.setSpeed(4, 100);
  cmd.readLocation(4);
}

void loop() {


  while (SerialUSB.available() == 9) { // Bps za SerialUSB=57600, potrebno ustrezno nastaviti v Termitu.
    bufer[0] = SerialUSB.read();
    bufer[1] = SerialUSB.read();
    bufer[2] = SerialUSB.read();
    bufer[3] = SerialUSB.read();
    bufer[4] = SerialUSB.read();
    bufer[5] = SerialUSB.read();
    bufer[6] = SerialUSB.read();
    bufer[7] = SerialUSB.read();
    bufer[8] = SerialUSB.read();

  }
  a = bufer[0];
  b = bufer[1];
  c = bufer[2];
  d = bufer[3];
  e = bufer[4];
  f = bufer[5];
  g = bufer[6];
  h = bufer[7];
  j = bufer[8];
  kot1=(b<<8)|(c);
  kot2=(d<<8)|(e);
  kot3=(f<<8)|(g);
  kot4=(h<<8)|(j);

  


  switch (a){
  case 0x08:
    torqueSend();
    break;
  case 0x09:
    cmd.setLocation(1,kot1);
    cmd.setLocation(2,kot2);
    cmd.setLocation(3,kot3);
    cmd.setLocation(4,kot4);
    break;
  }
  a = 999;
  
  navor1 = cmd.readTorque(1);
  if(navor1 >= 200 && navor1 <= 1000 || navor1 >= 1200 && navor1 <= 2000){
    if(imeCheckNavor==0){
    SerialUSB.println(5);
    imeCheckNavor=1;}
    
  }
  
  
  if(navor1 >= 0 && navor1 <= 100 || navor1 >= 1024 && navor1 <= 1200){
    if(imeCheckNavor==1){
    imeCheckNavor=0;
    //SerialUSB.println(6);
  }  
  }

}

void torqueSend(){
  navor1 = cmd.readTorque(1);
  navor2 = cmd.readTorque(2);
  navor3 = cmd.readTorque(3);
  navor4 = cmd.readTorque(4);
  if(navor1 >= 200 && navor1 <= 1000 || navor1 >= 1200 && navor1 <= 2000){
    SerialUSB.println("1000");
  }
//  SerialUSB.print(navor1);
//  SerialUSB.print("x");
//  SerialUSB.print(navor2);
//  SerialUSB.print("x");
//  SerialUSB.print(navor3);
//  SerialUSB.print("x");
//  SerialUSB.println(navor4);
}




