//Created by Klemen Štrajhar

#include <robolib.h>
#define interval 1000

//Spremenljivke
int bufer[9];
int a, b, c, d, e, f, g, h, i, j;
int kot1=512, kot2 = 300, kot3 = 300, kot4 = 500;
int navor1, navor2, navor3, navor4;
int ID;
int navor;
int hitrost;
int zacetek = 0;
int konec;
int temp;
bool movingXNavor = 0, movingNavor = 0;
int speed = 70;
int kotP1, kotP2, kotP3, kotP4;
int kotM1 = 512, kotM2 = 150, kotM3=300, kotM4 = 300;
int kotM1_2 = 512, kotM2_2 = 145, kotM3_2=115, kotM4_2 = 470;
int limit1 = 220, limit2 = 150, limit3 = 450, limit4 = 270;
int limit1_m = 220, limit2_m = 150, limit3_m = 500, limit4_m = 300;

byte torq1;
char dataToBeSent[9];
int motorData[8];
char test[9];

//Objekti
RobotControl cmd(3, 1);

//Funkcije
void prepareData();
void reactToTorque(int);
void reactToTorqueMoving();

void setup()
{
  SerialUSB.begin();
  cmd.setSpeed(1, speed);
  cmd.setSpeed(2, speed);
  cmd.setSpeed(3, speed);
  cmd.setSpeed(4, speed);

  cmd.setLocation(1, 512);
  cmd.setLocation(2, 300);
  cmd.setLocation(3, 300);
  cmd.setLocation(4, 500);

  cmd.setSpeed(1, speed + 40);
  cmd.setSpeed(2, speed + 40);
  cmd.setSpeed(3, speed + 60);
  cmd.setSpeed(4, speed + 60);
  kotP1 = 512; 
  kotP2 = 300; 
  kotP3= 300; 
  kotP4 = 500;
  pinMode(14,OUTPUT);
}

void loop()
{

  while (SerialUSB.available() == 9)
  { // Bps za SerialUSB=57600, potrebno ustrezno nastaviti v Termitu.

    a = SerialUSB.read();
    b = SerialUSB.read();
    c = SerialUSB.read();
    d = SerialUSB.read();
    e = SerialUSB.read();
    f = SerialUSB.read();
    g = SerialUSB.read();
    h = SerialUSB.read();
    j = SerialUSB.read();

  }


  kot1 = (b << 8) | (c);
  kot2 = (d << 8) | (e);
  kot3 = (f << 8) | (g);
  kot4 = (h << 8) | (j);

  test[0] = (cmd.readLocation(1) >> 8);
  test[1] = (cmd.readLocation(1) & 0xff);
  test[2] = (cmd.readLocation(2) >> 8);
  test[3] = (cmd.readLocation(2) & 0xff);
  test[4] = (cmd.readLocation(3) >> 8);
  test[5] = (cmd.readLocation(3) & 0xff);
  test[6] = (cmd.readLocation(4) >> 8);
  test[7] = (cmd.readLocation(4) & 0xff);
  test[8] = (byte) 4;

  navor1 = cmd.readTorque(1);
  navor2 = cmd.readTorque(2);
  navor3 = cmd.readTorque(3);
  navor4 = cmd.readTorque(4);
  //  if(((navor1 >= limit1) && (navor1 < 1024)) || ((navor1 >= 1024 + limit1) && (navor1 <= 2040))){
  //    reactToTorque(1);
  //    movingXNavor = 1;
  //  }
  //  if(((navor2 >= limit2) && (navor2 < 1024)) || ((navor2 >= 1024 + limit2) && (navor2 <= 2040))){
  //    //reactToTorque(2);
  //    movingXNavor = 1;
  //  }
  if((((navor3 >= limit3) && (navor3 < 1024)) || ((navor3 >= 1024 + limit4) && (navor3 <= 2040))) && (a == 9)){
    reactToTorque(3);
    movingXNavor = 1;
  }
  if((((navor4 >= limit4) && (navor4 < 1024)) || ((navor4 >= 1024 + limit4) && (navor4 <= 2040))) && (a == 9)){
    reactToTorque(4);
    movingXNavor = 1;
  }
  if((((navor3 >= limit3_m) && (navor3 < 1024)) || ((navor3 >= 1024 + limit3_m) && (navor3 <= 2040))) && (a == 8)){
    reactToTorqueMoving();
    movingNavor = 1;
  }
  if((((navor4 >= limit4_m) && (navor4 < 1024)) || ((navor4 >= 1024 + limit4_m) && (navor4 <= 2040))) && (a == 8)){
    reactToTorqueMoving();
    movingNavor = 1;
  }

  switch (a)
  {
  case 0x07:
    //Resetira alarm in se vrne v default pozicijo
    cmd.setLocation(1, kot1);
    cmd.setLocation(2, kot2);
    cmd.setLocation(3, kot3);
    cmd.setLocation(4, kot4);
    movingXNavor = 0;

    break;
  case 0x08:

    cmd.setLocation(1, kot1);
    cmd.setLocation(2, kot2);
    cmd.setLocation(3, kot3);
    cmd.setLocation(4, kot4);


    break;
  case 0x09:
    if (movingXNavor == 0){
      cmd.setLocation(1, kot1);
      cmd.setLocation(2, kot2);
      cmd.setLocation(3, kot3);
      cmd.setLocation(4, kot4);

      kotP1 = kot1; 
      kotP2 = kot2; 
      kotP3 = kot3; 
      kotP4 = kot4;
    }
    break;
  }

  if(movingXNavor == 0){
    digitalWrite(14,HIGH);
  }
  else if(movingXNavor == 1){
    digitalWrite(14,LOW);
  }

}


void reactToTorque(int index){
  int noviKot;
  switch(index){
  case 1:
    if (kot1 < kotP1){
      cmd.setLocation(1, kot1+60);
    }
    else if (kot1 > kotP1){
      cmd.setLocation(1, kot1-60);
    }
    break;
  case 2:
    if (kot2 < kotP2){
      cmd.setLocation(2, kot2+5);
    }
    else if (kot2 > kotP2){
      cmd.setLocation(2, kot2-5);
    }
    break;
  case 3:
    if (kot3 < kotP3){
      cmd.setLocation(3, kot3+60);
    }
    else if (kot3 > kotP3){
      cmd.setLocation(3, kot3-60);
    }
    break;
  case 4:
    if (kot4 < kotP4){
      cmd.setLocation(4, kot4+60);
    }
    else if (kot4 > kotP4){
      cmd.setLocation(4, kot4-60);
    }
    break;
  }
  //  cmd.setLocation(1, kotP1);
  //  cmd.setLocation(2, kotP2);
  //  cmd.setLocation(3, kotP3);

}
void reactToTorqueMoving()
{ 
  cmd.setSpeed(1, speed-40);
  cmd.setSpeed(2, speed-40);
  cmd.setSpeed(3, speed-40);
  cmd.setSpeed(4, speed+40);
  cmd.setLocation(1, kotM1_2);
  cmd.setLocation(2, kotM2_2);
  cmd.setLocation(3, kotM3_2);
  cmd.setLocation(4, kotM4_2);
  delay(700);
  cmd.setLocation(1, kotM1);
  cmd.setLocation(2, kotM2);
  cmd.setLocation(3, kotM3);
  cmd.setLocation(4, kotM4);
  delay(700);
  cmd.setLocation(1, kot1);
  cmd.setLocation(2, kot2);
  cmd.setLocation(3, kot3);
  cmd.setLocation(4, kot4);
  cmd.setSpeed(1, speed + 40);
  cmd.setSpeed(2, speed + 40);
  cmd.setSpeed(3, speed + 60);
  cmd.setSpeed(4, speed + 60);
  movingNavor = 0;
}












