from tkinter import *
import math as m
import matplotlib.pyplot as plt
import numpy as np
import serial
from mpl_toolkits.mplot3d import Axes3D
import serial.tools.list_ports
import time
import multiprocessing as mp
from queue import Queue

# globalna spremenljivkA
torque_alert = 0

# Incializacija seriala
ports = list(serial.tools.list_ports.comports())
port = []
ser = None
for p in ports:
    p = str(p)
    port.append(p)

for i in range(len(port)):
    if "ROBOTIS" in port[i]:
        a = port[i]
        real_port = a[0:4]
        print(real_port)
        ser = serial.Serial(real_port, baudrate=115200, timeout=1)


class Application(Frame):
    def createWidgets(self):
        """
        Naredi Tkinter GUI
        :return: void
        """
        # print(ser.readline().decode("ascii"))

        labelhello = Label(root, text="Welcome to leg controller")
        labelhello.grid(row=0, columnspan=6)

        label1 = Label(root, text="Motor 1")
        label2 = Label(root, text="Motor 2")
        label3 = Label(root, text="Motor 3")
        label4 = Label(root, text="Motor 4")

        label1.grid(row=3)
        label2.grid(row=4)
        label3.grid(row=5)
        label4.grid(row=6)

        label_speed = Label(root, text="Angle")
        label_torque = Label(root, text="Torque")

        label_speed.grid(row=2, column=1)
        label_torque.grid(row=2, column=4)

        self.entry1 = Entry(root)
        self.entry2 = Entry(root)
        self.entry3 = Entry(root)
        self.entry4 = Entry(root)
        self.entry5 = Entry(root)
        self.entry6 = Entry(root)
        self.entry7 = Entry(root)
        self.entry8 = Entry(root)

        self.entry1.grid(row=3, column=1)
        self.entry2.grid(row=3, column=4)
        self.entry3.grid(row=4, column=1)
        self.entry4.grid(row=4, column=4)
        self.entry5.grid(row=5, column=1)
        self.entry6.grid(row=5, column=4)
        self.entry7.grid(row=6, column=1)
        self.entry8.grid(row=6, column=4)

        gumb1 = Button(root, text="Send", command=self.readingFromApp1)
        gumb2 = Button(root, text="Send", command=self.readingFromApp2)
        gumb3 = Button(root, text="Send", command=self.readingFromApp3)
        gumb4 = Button(root, text="Send", command=self.readingFromApp4)
        gumb1.grid(row=3, column=5)
        gumb2.grid(row=4, column=5)
        gumb3.grid(row=5, column=5)
        gumb4.grid(row=6, column=5)

        label_coord = Label(root, text="  ")
        label_coord.grid(row=7, columnspan=6)

        label_coord1 = Label(root, text="Vpis koordinat")
        label_coord1.grid(row=8, columnspan=6)

        label_time = Label(root, text="Čas premikanja")
        label_time.grid(row=7)
        self.entry_time = Entry(root)
        self.entry_time.grid(row=7, column=1)

        label_coord1 = Label(root, text="X")
        label_coord1.grid(row=10, columnspan=2)
        label_coord1 = Label(root, text="Y")
        label_coord1.grid(row=10, columnspan=2, column=2)
        label_coord1 = Label(root, text="Z")
        label_coord1.grid(row=10, columnspan=2, column=4)

        self.xentry = Entry(root)
        self.xentry.grid(row=11, columnspan=2)
        self.yentry = Entry(root)
        self.yentry.grid(row=11, columnspan=2, column=2)
        self.zentry = Entry(root)
        self.zentry.grid(row=11, columnspan=2, column=4)
        gumb_koord = Button(root, text="Poslji koordinate", command=self.moving)
        gumb_koord.grid(row=12, columnspan=6)

        label_coord1 = Label(root, text="  ")
        label_coord1.grid(row=13, columnspan=6)

        gumb_default = Button(root, text='Reset pozicije', command=self.reset)
        gumb_default.grid(row=14, columnspan=6)

        labelemp = Label(root, text=" ")
        labelemp.grid(row=15, columnspan=6)

        labelemp = Label(root, text=" ")
        labelemp.grid(row=16, columnspan=6)

        navor_label_1 = Label(root, text="Navor M1")
        navor_label_2 = Label(root, text="Navor M2")
        navor_label_3 = Label(root, text="Navor M3")
        navor_label_4 = Label(root, text="Navor M4")

        navor_label_1.grid(row=16, column=1)
        navor_label_2.grid(row=16, column=2)
        navor_label_3.grid(row=16, column=3)
        navor_label_4.grid(row=16, column=4)

        self.navor_1 = Text(root, height=1, width=10)
        self.navor_2 = Text(root, height=1, width=10)
        self.navor_3 = Text(root, height=1, width=10)
        self.navor_4 = Text(root, height=1, width=10)

        self.navor_1.grid(row=17, column=1)
        self.navor_2.grid(row=17, column=2)
        self.navor_3.grid(row=17, column=3)
        self.navor_4.grid(row=17, column=4)

        frame = Frame(root)
        root.bind("<Up>", self.Xup)
        root.bind("<Down>", self.Xdown)
        root.bind("<Left>", self.Yup)
        root.bind("<Right>", self.Ydown)
        root.bind("<Prior>", self.Zup)
        root.bind("<Next>", self.Zdown)
        frame.grid()

    def sendAngles(self):
        kot1H = (self.kot1 >> 8) & 255
        kot1L = self.kot1 & 255
        kot2H = (self.kot2 >> 8) & 255
        kot2L = self.kot2 & 255
        kot3H = (self.kot3 >> 8) & 255
        kot3L = self.kot3 & 255
        kot4H = (self.kot4 >> 8) & 255
        kot4L = self.kot4 & 255
        data = ([9, kot1H, kot1L, kot2H, kot2L, kot3H, kot3L, kot4H, kot4L])
        # print(self.kot1, self.kot2, self.kot3, self.kot4)
        ser.write(data)
        inputSer = ser.readline().decode('utf8')
        inputSer = int(inputSer)
        limit = 150
        if inputSer >= limit and inputSer < 1024 or inputSer >= 1024 + limit and inputSer < 2040:
            if self.torqueOverload == 0:
                self.torqueOverload = 1
                print("Overload")

        if inputSer >= 0 and inputSer < limit or inputSer >= 1024 and inputSer < 1024 + limit:
            if self.torqueOverload == 1:
                self.torqueOverload = 0
                # print(inputSer)

        self.after(5, self.sendAngles)

    def Xup(self, event):

        self.xb = self.xb + self.i
        self.movingX()

    def Xdown(self, event):
        self.xb = self.xb - self.i
        # if self.xb < 50:
        #     self.xb = 50
        self.movingX()

    def Yup(self, event):
        self.yb = self.yb + self.i
        self.movingX()

    def Ydown(self, event):
        self.yb = self.yb - self.i
        self.movingX()

    def Zup(self, event):
        self.zb = self.zb + self.i
        self.movingX()

    def Zdown(self, event):
        self.zb = self.zb - self.i
        self.movingX()

    def ForwardVectors(self, PA, PB,
                       l):  # PA je prve točka vektorja, PB je točka proti kateri gre vektor. l je dolžina vektorja.
        Vektor = -PA + PB
        Vektor_enotski = Vektor / m.sqrt(Vektor[0] ** 2 + Vektor[1] ** 2)
        Vektor_i = Vektor_enotski * l
        Pi = Vektor_i + PA
        return Pi

    def read_data(self, input):
        b = [index for index, value in enumerate(input) if value == "x"]
        kot1 = int(input[0:b[0]])
        kot2 = int(input[b[0] + 1:b[1]])
        kot3 = int(input[b[1] + 1:b[2]])
        kot4 = int(input[b[2] + 1:])
        return kot1, kot2, kot3, kot4

    def razdaljainkot(self, PA, PC, la, lb):
        dist = m.sqrt((PC[0] - PA[0]) ** 2 + (PC[1] - PA[1]) ** 2)
        try:
            q = m.acos((dist ** 2 - la ** 2 - lb ** 2) / (-2 * la * lb))
            return q
        except Exception:
            print("Izven delovnega območja")

    def angle_side(self, P_1, P_2, P_3, i):
        k = (P_2[1] - P_1[1]) / (P_2[0] - P_1[0])
        fun_org = k * (P_3[0] - P_1[0]) + P_1[1]  # Dobimo vrednost funkcije, če za x vstavimo P_3[0]
        if i == 1:
            if k >= 0:
                if fun_org <= P_3[1]:
                    predznak = -1
                elif fun_org > P_3[1]:
                    predznak = 1
            elif k < 0:
                if fun_org < P_3[1]:
                    predznak = 1
                elif fun_org > P_3[1]:
                    predznak = -1

        if i == 2:
            if k >= 0:
                if fun_org <= P_3[1]:
                    predznak = -1
                elif fun_org > P_3[1]:
                    predznak = 1
            elif k < 0:
                if fun_org <= P_3[1]:
                    predznak = 1
                elif fun_org > P_3[1]:
                    predznak = 1
        return predznak

    def reset(self):  # Puts the robot to the starting position
        self.kot1 = 512
        self.kot2 = 300
        self.kot3 = 300
        self.kot4 = 300
        kot1H = (self.kot1 >> 8) & 255
        kot1L = self.kot1 & 255
        kot2H = (self.kot2 >> 8) & 255
        kot2L = self.kot2 & 255
        kot3H = (self.kot3 >> 8) & 255
        kot3L = self.kot3 & 255
        kot4H = (self.kot4 >> 8) & 255
        kot4L = self.kot4 & 255
        data = ([9, kot1H, kot1L, kot2H, kot2L, kot3H, kot3L, kot4H, kot4L])
        print(self.kot1, self.kot2, self.kot3, self.kot4)
        ser.write(data)

    def readingFromApp1(self):
        motor = 1
        speed = int(self.entry1.get())
        torque = int(self.entry2.get())
        pByte_speed = (speed >> 8) & 255
        dByte_speed = speed & 255
        pByte_torque = (torque >> 8) & 255
        dByte_torque = torque & 255
        data = ([motor, pByte_speed, dByte_speed, pByte_torque, dByte_torque, 0, 0, 0, 0])
        ser.write(data)
        print(ser.readline().decode("ascii"))

    def readingFromApp2(self):
        motor = 2
        speed = int(self.entry3.get())
        torque = int(self.entry4.get())
        pByte_speed = (speed >> 8) & 255
        dByte_speed = speed & 255
        pByte_torque = (torque >> 8) & 255
        dByte_torque = torque & 255
        data = ([motor, pByte_speed, dByte_speed, pByte_torque, dByte_torque, 0, 0, 0, 0])
        ser.write(data)
        print(ser.readline().decode("ascii"))

    def readingFromApp3(self):
        motor = 3
        speed = int(self.entry5.get())
        torque = int(self.entry6.get())
        pByte_speed = (speed >> 8) & 255
        dByte_speed = speed & 255
        pByte_torque = (torque >> 8) & 255
        dByte_torque = torque & 255
        data = ([motor, pByte_speed, dByte_speed, pByte_torque, dByte_torque, 0, 0, 0, 0])
        ser.write(data)
        print(ser.readline().decode("ascii"))

    def readingFromApp4(self):
        motor = 4
        speed = int(self.entry7.get())
        torque = int(self.entry8.get())
        pByte_speed = (speed >> 8) & 255
        dByte_speed = speed & 255
        pByte_torque = (torque >> 8) & 255
        dByte_torque = torque & 255
        data = ([motor, pByte_speed, dByte_speed, pByte_torque, dByte_torque, 0, 0, 0, 0])
        ser.write(data)
        print(ser.readline().decode("ascii"))

    def speedCalculate(self, KOT1, KOT2, time):
        delta = abs(KOT2 - KOT1)
        fi = (300 / 1023 * delta)  # Stopinje
        ang_velocity = m.radians(fi) / time
        rpm = ang_velocity / (2 * m.pi / 60)
        rpm_int = round(rpm / 0.111)
        return rpm_int

    def movingX(self):
        """
        Izvede preračun za novo pozicijo in jo preko klica ser.write() pošlje na mikrokrmilnik.
        :return: 
        """
        time1 = time.clock()
        x = self.xb  # - self.ix
        y = self.yb
        z = self.zb  # - self.h
        if x ** 2 + y ** 2 + z ** 2 <= 67600:
            q2 = m.radians(int(90))
            q3 = m.radians(int(45))
            q4 = m.radians(int(45))

            P1i = np.array(([0, 0]))
            P2i = np.array([self.l1 * m.cos(q2), self.l1 * m.sin(q2)])
            P3i = np.array(
                [self.l1 * m.cos(q2) + self.l2 * m.cos(q2 - q3), self.l1 * m.sin(q2) + self.l2 * m.sin(q2 - q3)])
            P4i = np.array([self.l1 * m.cos(q2) + self.l2 * m.cos(q2 - q3) + self.l3 * m.cos(q2 - q3 - q4),
                            self.l1 * m.sin(q2) + self.l2 * m.sin(q2 - q3) + self.l3 * m.sin(q2 - q3 - q4)])

            G = np.array([m.sqrt(y ** 2 + x ** 2), z])
            P4ii = G
            for i in range(0, 100):
                P4i = G
                P3i = self.ForwardVectors(P4i, P3i, self.l3)
                P2i = self.ForwardVectors(P3i, P2i, self.l2)
                P1i = self.ForwardVectors(P2i, P1i, self.l1)

                P1ii = np.array([0, 0])
                P2ii = self.ForwardVectors(P1ii, P2i, self.l1)
                P3ii = self.ForwardVectors(P2ii, P3i, self.l2)
                P4ii = self.ForwardVectors(P3ii, G, self.l3)

                # Določitev novih vrednosti za novo zanko.
                P1i = P1ii
                P2i = P2ii
                P3i = P3ii
                P4i = P4ii
                # Izračun napake
                errx = abs(P4i[[0]] - G[[0]])
                errz = abs(P4i[[1]] - G[[1]])
                if errx < 0.01 and errz < 0.01:
                    break

            q1 = m.degrees(m.atan2(y, x))
            q2 = m.degrees(m.atan2(P2i[1], P2i[0]))
            q3 = 180 - m.degrees(self.razdaljainkot(P1i, P3i, self.l1, self.l2))
            q4 = 180 - m.degrees(self.razdaljainkot(P2i, P4i, self.l2, self.l3))

            if self.angle_side(P1i, P2i, P3i, 1) == 1:
                q3 = q3
            elif self.angle_side(P1i, P2i, P3i, 1) == -1:
                q3 = -q3

            if self.angle_side(P2i, P3i, P4ii, 2) == 1:
                q4 = q4
            elif self.angle_side(P2i, P3i, P4i, 2) == -1:
                q4 = -q4

            if q2 < 0:
                q3 = -q3

            self.q11 = q1
            self.q22 = q2
            self.q33 = q3
            self.q44 = q4

            self.kot1 = round(512 + (1023 / 300 * q1))
            self.kot2 = round(480 - (1023 / 300 * q2))
            self.kot3 = round(485 - (1023 / 300 * q3))
            self.kot4 = round(180 + (1023 / 300 * q4))

            # kot1H = (kot1 >> 8) & 255
            # kot1L = kot1 & 255
            # kot2H = (kot2 >> 8) & 255
            # kot2L = kot2 & 255
            # kot3H = (kot3 >> 8) & 255
            # kot3L = kot3 & 255
            # kot4H = (kot4 >> 8) & 255
            # kot4L = kot4 & 255
            # data = ([9, kot1H, kot1L, kot2H, kot2L, kot3H, kot3L, kot4H, kot4L])
            # ser.write(data)
            # incoming_Stream = ser.readline().decode("utf8")
            # print(incoming_Stream)
            print('Pozicija x: {}, y: {}, z: {}'.format(self.xb, self.yb, self.zb))
            print('Kot 1: {0:.3f}°, kot 2: {1:.3f}°, kot 3: {2:.3f}°, kot 4: {3:.3f}°'.format(q1, q2, q3, q4))
            q1 = np.radians(q1)
            q2 = np.radians(q2)
            q3 = -np.radians(q3)
            q4 = -np.radians(q4)
            xa = (60 * np.cos(q2) + 60 * np.cos(q2 + q3) + 150 * np.cos(q2 + q3 + q4)) * m.cos(q1)
            za = 60 * np.sin(q2) + 60 * np.sin(q2 + q3) + 150 * np.sin(q2 + q3 + q4)
            ya = np.tan(q1) * xa
            print('Napake x: {0:.5f}, y:{1:.5f}, z:{2:.5f} [mm]'.format(abs(xa - self.xb), abs(ya - self.yb),
                                                                        abs(za - self.zb)))
            time2 = time.clock()
            cas = (time2 - time1) * 10 ** 3
            print("Čas za eksekucijo programa je %0.6f ms" % cas)
            print('Število iteracij {}'.format(i))
            print("  ")

        else:
            print("Koordinata izven dosegljivega območja", x ** 2 + y ** 2 + z ** 2)

    def moving(self):
        time1 = time.clock()
        x = int(self.xentry.get())  # -self.ix
        y = int(self.yentry.get())
        z = int(self.zentry.get())  # -self.h
        # Začetni pogoji

        if x ** 2 + y ** 2 + z ** 2 <= 67600:
            q2 = m.radians(int(90))
            q3 = m.radians(int(45))
            q4 = m.radians(int(45))

            P1i = np.array(([0, 0]))
            P2i = np.array([self.l1 * m.cos(q2), self.l1 * m.sin(q2)])
            P3i = np.array(
                [self.l1 * m.cos(q2) + self.l2 * m.cos(q2 - q3), self.l1 * m.sin(q2) + self.l2 * m.sin(q2 - q3)])
            P4i = np.array([self.l1 * m.cos(q2) + self.l2 * m.cos(q2 - q3) + self.l3 * m.cos(q2 - q3 - q4),
                            self.l1 * m.sin(q2) + self.l2 * m.sin(q2 - q3) + self.l3 * m.sin(q2 - q3 - q4)])

            G = np.array([m.sqrt(y ** 2 + x ** 2), z])
            P4ii = G
            for i in range(0, 100):
                P4i = G
                P3i = self.ForwardVectors(P4i, P3i, self.l3)
                P2i = self.ForwardVectors(P3i, P2i, self.l2)
                P1i = self.ForwardVectors(P2i, P1i, self.l1)

                P1ii = np.array([0, 0])
                P2ii = self.ForwardVectors(P1ii, P2i, self.l1)
                P3ii = self.ForwardVectors(P2ii, P3i, self.l2)
                P4ii = self.ForwardVectors(P3ii, G, self.l3)

                # Določitev novih vrednosti za novo zanko.
                P1i = P1ii
                P2i = P2ii
                P3i = P3ii
                P4i = P4ii
                # Izračun napake
                errx = abs(P4i[[0]] - G[[0]])
                errz = abs(P4i[[1]] - G[[1]])
                if errx < 0.01 and errz < 0.01:
                    break

            q1 = m.degrees(m.atan2(y, x))
            q2 = m.degrees(m.atan2(P2i[1], P2i[0]))
            q3 = 180 - m.degrees(self.razdaljainkot(P1i, P3i, self.l1, self.l2))
            q4 = 180 - m.degrees(self.razdaljainkot(P2i, P4i, self.l2, self.l3))

            if self.angle_side(P1i, P2i, P3i, 1) == 1:
                q3 = q3
            elif self.angle_side(P1i, P2i, P3i, 1) == -1:
                q3 = -q3

            if self.angle_side(P2i, P3i, P4ii, 2) == 1:
                q4 = q4
            elif self.angle_side(P2i, P3i, P4i, 2) == -1:
                q4 = -q4

            if q2 < 0:
                q3 = -q3

            # if q3>90:
            #     q4=-q4

            self.q11 = q1
            self.q22 = q2
            self.q33 = q3
            self.q44 = q4

            self.kot1 = round(512 + (1023 / 300 * q1))
            self.kot2 = round(480 - (1023 / 300 * q2))
            self.kot3 = round(485 - (1023 / 300 * q3))
            self.kot4 = round(180 + (1023 / 300 * q4))

            # kot1H = (kot1 >> 8) & 255
            # kot1L = kot1 & 255
            # kot2H = (kot2 >> 8) & 255
            # kot2L = kot2 & 255
            # kot3H = (kot3 >> 8) & 255
            # kot3L = kot3 & 255
            # kot4H = (kot4 >> 8) & 255
            # kot4L = kot4 & 255
            # data = ([9, kot1H, kot1L, kot2H, kot2L, kot3H, kot3L, kot4H, kot4L])
            # ser.write(data)


            # print('Pozicija x: {}, y: {}, z: {}'.format(self.xb, self.yb, self.zb))
            # print('Kot 1: {0:.3f}°, kot 2: {1:.3f}°, kot 3: {2:.3f}°, kot 4: {3:.3f}°'.format(q1, q2, q3, q4))
            # q1 = np.radians(q1)
            # q2 = np.radians(q2)
            # q3 = -np.radians(q3)
            # q4 = -np.radians(q4)
            # xa = (60 * np.cos(q2) + 60 * np.cos(q2 + q3) + 150 * np.cos(q2 + q3 + q4)) * m.cos(q1)
            # za = 60 * np.sin(q2) + 60 * np.sin(q2 + q3) + 150 * np.sin(q2 + q3 + q4)
            # ya = np.tan(q1) * xa
            # print('Napake x: {0:.5f}, y:{1:.5f}, z:{2:.5f} [mm]'.format(abs(xa - self.xb), abs(ya - self.yb),
            #                                                             abs(za - self.zb)))
            # print(np.sqrt(x ** 2 + y ** 2 + z ** 2))
            # time2 = time.clock()
            # cas = (time2 - time1) * 10 ** 3
            # print("Čas za eksekucijo programa je %0.6f ms" % cas)
            # print('Število iteracij {}'.format(i))
            # print("  ")



        else:
            print("Koordinata izven dosegljivega območja", x ** 2 + y ** 2 + z ** 2)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        # Spremenljivke
        self.xb = 150
        self.yb = 0
        self.zb = -50
        self.i = 5  # Velikost koraka premika [mm]
        self.h = 295
        self.ix = 50

        self.l1 = 60
        self.l2 = 60
        self.l3 = 150

        self.q11 = 0
        self.q22 = 90
        self.q33 = 45
        self.q44 = 45
        print("Started main thread")

        self.kot1 = 512
        self.kot2 = 300
        self.kot3 = 300
        self.kot4 = 500

        self.torqueOverload = 0
        self.createWidgets()
        self.sendAngles()

        self.index = 0
        self.id = None


if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.mainloop()

    ser.close()
