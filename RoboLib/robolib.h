#ifndef ROBOLIB_H
#define ROBOLIB_H
#include "Dynamixel.h"

class RobotControl: public Dynamixel
{
  public:
    //Constructor
    RobotControl(int bType, int bRate); 
    /*
    Constructor prejme dva parametra. Prvi je tip plošče, ki se jo uporablja
    bType = 1, če se uporablja samo ploščo openCM 9.04
    bType = 3, če se uporablja še razširitvena plošča OpenCM 485 EXP
    
    bRate je nastavitev Baud ratea po principu
    0: 9600bps, 1: 57600bps, 2: 115200bps, 3: 1Mbps
    */
    
    // Setter functions
    void setLocation(uint8 ID, int location);
    /*
    Funkcija setLocation pošlje ukaz motorju, da se premakne na željeno lokacijo.
    ID parameter sprejme id motorja.
    location sprejme željeno pozicijo motorja, ki mora biti v rangu 0-1023 (0°-300°)
    primer:
    objekt.setLocation(1,500) pošlje motor z ID 1 na lokacijo 500.
    */
    
    void setSpeed(uint8 ID, int speed);
    /*
    Funkcija setSpeed pošlje ukaz motorju, da spremeni obratovalno hitrost.
    ID parameter sprejme id motorja.
    speed sprejme željeno hitrost motorja, ki mora biti v rangu 0-1023 (občutljivost je 0.111rpm)
    primer:
    objekt.setSpeed(1,300) nastavi hitrost motorja z ID 1 na 33.3rpm.
    */
    
    void setTorque(uint8 ID, int torque);
    /*
    Funkcija setSpeed pošlje ukaz motorju, da spremeni obratovalno hitrost.
    ID parameter sprejme id motorja.
    torque sprejme željeni navor motorja, ki mora biti v rangu 0-1023 (občutljivost je 0.1%)
    primer:
    objekt.setTorque(1,300) nastavi navor motorja z ID 1 na 30% maksimalne vrednosti.
    */
    
    void torqueOnOff(uint8 ID, int setting);
    /*
    Funkcija torqueOnOff pošlje ukaz motorju, da se upira spemembam pozicije.
    ID parameter sprejme id motorja.
    setting sprejme 1 za vklop navora in 0 za izklop navora
    primer:
    objekt.torqueOnOff(1,1) vključi navor za motor 1
    */
    
    // Reader functions
    int readLocation(uint8 ID);
    /*
    Prebere lokacijo motorja z izbranim ID.
    Vrne vrednost med 0-1023
    */
    
    int readSpeed(uint8 ID);
    /*
    Prebere nastavljeno hitrost motorja z izbranim ID.
    Vrne vrednost med 0-1023
    */
    
    int readTorque(uint8 ID);
    /*
    Prebere obremenitev motorja z izbranim ID.
    Vrne vrednost med 0-2047. Če je vrednost v območju 0-1023, je obremenitev usmerjena v nasprotni smeri urinega kazalca.
    Če je vrednost v območju 1024-2047 je obremenitev usmerjena v smeri urinega kazalca.
    */
    
  private:
    // private spremenljivke, da se jih pomotoma ne da spreminjati.
    int boardType;
    int baudRate;
};

#endif
