
import runloop,motor,force_sensor,time,motor_pair
from hub import port as port
pi=3.1415926535
radius_wheel_mm=55.5
globalStopMovement = 0
async def delay(delay1):
    if (globalStopMovement == 0):
        class delayclass():
            def __init__(self):
                self.lastTimeButton = time.ticks_ms()
                self.tlacitkoL = port.C
                self.tlacitkoP = port.D
                self.delayStop = 0
                self.buttonFaze = self.buttonDetect
                self.lastTimedelay = time.ticks_ms()
            def buttonDetect(self):
                if (force_sensor.force(self.tlacitkoL) >= 40 and force_sensor.force(self.tlacitkoP) >= 40):
                    self.lastTimeButton = time.ticks_ms()
                    self.buttonFaze = self.buttonChecker
            def buttonChecker(self):
                if not(force_sensor.force(self.tlacitkoL) >= 40 and force_sensor.force(self.tlacitkoP) >= 40):
                    self.buttonFaze = self.buttonDetect
                elif (force_sensor.force(self.tlacitkoL) >= 40 and force_sensor.force(self.tlacitkoP) >= 40):
                    if(self.lastTimeButton + 0.5 <= time.ticks_ms()):
                        self.delayStop = 1
                        global globalStopMovement
                        globalStopMovement = 1
            def delay2(self):
                if (self.lastTimedelay + abs(delay1) <= time.ticks_ms()):
                    self.delayStop = 1
        task1 = delayclass()
        task2 = delayclass()
        while not(task1.delayStop == 1 or task2.delayStop or globalStopMovement == 1):
            task1.buttonFaze()
            task2.delay2()
async def movement(ver,port1,port2,speed,rotation_234speed,distance_cm):
    speed1 = speed
    speed2 = rotation_234speed
    if (globalStopMovement == 0):
        class movementclass:
            def __init__ (self):
                self.tlacitkoL = port.C
                self.tlacitkoP = port.D
                self.stupne=round(360*distance_cm/(radius_wheel_mm*pi/10))
                self.lastPosL = motor.relative_position(port1)
                self.lastPosP = motor.relative_position(port2)
                self.motorStop = 0
                self.acceleration = 2000
                self.lastTimeButton = time.ticks_ms()
                if(ver==1):
                    self.movementFaze = self.startMotors1
                    self.buttonFaze = self.buttonDetect
                elif (ver==2):
                    self.movementFaze = self.startMotors2
                    self.buttonFaze = self.buttonDetect
                elif (ver==3):
                    self.movementFaze = self.startMotors3
                    self.buttonFaze = self.buttonDetect
                elif (ver==4):
                    self.movementFaze = self.startMotors4
                    self.buttonFaze = self.buttonDetect
                else:
                    print("ERROR: movement function: invaild parameter → ver")
            def buttonDetect(self):
                if (force_sensor.force(self.tlacitkoL) >= 40 and force_sensor.force(self.tlacitkoP) >= 40):
                    self.lastTimeButton = time.ticks_ms()
                    self.buttonFaze = self.buttonChecker
            def buttonChecker(self):
                if not(force_sensor.force(self.tlacitkoL) >= 40 and force_sensor.force(self.tlacitkoP) >= 40):
                    self.buttonFaze = self.buttonDetect
                elif (force_sensor.force(self.tlacitkoL) >= 40 and force_sensor.force(self.tlacitkoP) >= 40):
                    if(self.lastTimeButton + 0.5 <= time.ticks_ms()):
                        self.motorStop = 1
                        motor.stop(port1,stop=motor.BRAKE)
                        motor.stop(port2,stop=motor.BRAKE)
                        global globalStopMovement
                        globalStopMovement = 1
            def startMotors1(self):
                motor_pair.pair(motor_pair.PAIR_1,port1,port2)
                motor_pair.move(motor_pair.PAIR_1,speed2,velocity=speed1,acceleration=self.acceleration)
                motor_pair.unpair(motor_pair.PAIR_1)
                self.movementFaze = self.checkMotors1
            def checkMotors1(self):
                currentPosL = motor.relative_position(port1)
                currentPosP = motor.relative_position(port2)
                if (((currentPosL<=self.lastPosL - self.stupne and speed1>0) or (currentPosP>=self.lastPosP +self.stupne and speed1>0))or ((currentPosL>=self.lastPosL + self.stupne and speed1<0) or (currentPosP<=self.lastPosP - self.stupne and speed1<0))):
                    motor.stop(port1,stop=motor.BRAKE)
                    motor.stop(port2,stop=motor.BRAKE)
                    self.motorStop = 1
            def startMotors2(self):
                motor.run(port1,-(speed1),acceleration=self.acceleration)
                self.movementFaze = self.checkMotors2
            def checkMotors2(self):
                self.currentPosL = motor.relative_position(port1)
                if ((self.lastPosL - self.stupne >= self.currentPosL and speed1>0) or (self.lastPosL + self.stupne <= self.currentPosL and speed1<0)):
                    motor.stop(port1,stop=motor.BRAKE)
                    self.motorStop = 1
            def startMotors3(self):
                motor.run(port2,speed2,acceleration=self.acceleration)
                self.movementFaze = self.checkMotors3
            def checkMotors3(self):
                currentPosP = motor.relative_position(port2)
                if ((self.lastPosP + self.stupne <= currentPosP and speed2>0) or (self.lastPosP - self.stupne >= currentPosP and speed2<0)):
                    motor.stop(port2,stop=motor.BRAKE)
                    self.motorStop = 1
            def startMotors4(self):
                motor.run(port1,-(speed1),acceleration=self.acceleration)
                motor.run(port2,(speed2),acceleration=self.acceleration)
                self.movementFaze = self.checkMotors4
            def checkMotors4(self):
                currentPosL = motor.relative_position(port1)
                currentPosP = motor.relative_position(port2)
                if ((speed1<0) and (self.lastPosL - self.stupne >= currentPosL) or (self.lastPosP + self.stupne <= currentPosP)and(speed2>0) or (speed1<0) and (self.lastPosL + self.stupne <= currentPosL) or (self.lastPosP - self.stupne >= currentPosP)and(speed2<0)):
                    motor.stop(port1,stop=motor.BRAKE)
                    motor.stop(port2,stop=motor.BRAKE)
                    self.motorStop = 1
        if (distance_cm < 0):
            speed1 = -speed1
            speed2 = -speed2
            distance_cm = -distance_cm
        task1 = movementclass()
        while not(task1.motorStop == 1 or globalStopMovement == 1):
            task1.movementFaze()
            task1.buttonFaze()
async def movementdelay(ver,port1,port2,speed,rotation_234speed,distance_cm,delay1):
    await delay(delay1)
    await movement(ver,port1,port2,speed,rotation_234speed,distance_cm)



async def main():
    print("")
runlooport.run(main())

