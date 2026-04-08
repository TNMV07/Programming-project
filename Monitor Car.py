from machine import Pin, PWM
import network
import time
import espnow

#Network
wlan =  network.WLAN(network.STA_IF)
wlan.active(True)

#ESP_Now
e = espnow.ESPNow()
e.active(True)

#MAC
print(wlan.config("mac"))
print("CAR ACTIVATED!")

#Monitor-Car_Input
ENA = PWM(Pin(33), freq = 1000)
IN1 = Pin(25, Pin.OUT)
IN2 = Pin(26, Pin.OUT)
IN3 = Pin(27, Pin.OUT)
IN4 = Pin(14, Pin.OUT)
ENB = PWM(Pin(13), freq =1000)

#Camera_x-axis_Input
servo_x = PWM(Pin(18), Pin.OUT)
servo_x.init(freq = 50)

#Camera_y-axis_Input
servo_y = PWM(Pin(19), Pin.OUT)
servo_y.init(freq = 50)

#Servo Control Module
class servo_module:
    def __init__(self,x2, y2):
        self.x2 = servo_x
        self.y2 = servo_y
        
    #Control Function   
    def servo_control(self, x, y):
        sx = int((1 - (x / 4059)) * 102 + 26)
        sy = int((y / 4059) * 102 + 26)
        
        # Deadzone
        if sx < 10: sx = 0
        elif sy < 10: sy = 0
        
        #Overshoot
        if sx > 128: sx = 128
        elif sy > 128: sy =128
        
        #Servo angle
        self.x2.duty(sx)
        self.y2.duty(sy)
        
#Car Control Module  
class motor_module:
    def __init__(self, ENA, IN1, IN2, IN3, IN4, ENB):
        self.ENA = ENA
        self.IN1 = IN1
        self.IN2 = IN2
        self.IN3 = IN3
        self.IN4 = IN4
        self.ENB = ENB
    #Stop
    def stop(self, bt):
        self.ENA.duty(0)
        self.ENB.duty(0)
    
    #Control Function
    def control(self,x,y):
     
        #Set center
        dx = 2000 - x
        dy = 2000 - y
    
        #To avoid jerking
        if abs(dx) < 200: dx = 0
        if abs(dy) < 200: dy = 0
    
        #To determine velocity
        left_speed = int((dy - dx)/2)
        right_speed = int((dy + dx)/2)
       
        #To avoid overshoot (-1023, 1023)
        if left_speed > 1023:
            left_speed = 1023
        elif left_speed < -1023:
            left_speed = -1023
    
        if right_speed > 1023:
            right_speed = 1023
        elif right_speed < -1023:
            right_speed = -1023
        
        #Motors direction
        if left_speed >= 0:
            self.IN1.on(); self.IN2.off()
        else:
            self.IN1.off(); self.IN2.on()
    
        if right_speed >= 0:
            self.IN3.on(); self.IN4.off()
        else:
            self.IN3.off(); self.IN4.on()
            
        #Motors speed
        self.ENA.duty(abs(left_speed))
        self.ENB.duty(abs(right_speed))

#Main Loop 
car = motor_module(ENA, IN1, IN2, IN3, IN4, ENB)
camera = servo_module(servo_x, servo_y)
while True:
    
    #Receiving data
    host, msg = e.recv()
    
    #Decoding
    if msg:
        try:
            data = msg.decode().split (",")
            x1, y1, x2, y2, bt1, bt2 = map(int, data)
            
            #Car Control
            car.control (x1, y1)
            
            #Camera Control
            camera.servo_control (x2, y2)
        
        except:
            pass