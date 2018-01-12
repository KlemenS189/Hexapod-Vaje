#include "robolib.h"

RobotControl cmd(3,1);
int kot1,kot2,kot3,kot4;
void setup() {
  // put your setup code here, to run once:
    SerialUSB.begin();
    
}

void loop() {
  kot1 = cmd.readLocation(1);
  kot2 = cmd.readLocation(2);
  kot3 = cmd.readLocation(3);
  kot4 = cmd.readLocation(4);
  SerialUSB.print(kot1);
  SerialUSB.print("x");
  SerialUSB.print(kot2);
  SerialUSB.print("x");
  SerialUSB.print(kot3);
  SerialUSB.print("x");
  SerialUSB.println(kot4);
  delay(10);

}

