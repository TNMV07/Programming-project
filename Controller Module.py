from machine import ADC, Pin
import network
import espnow
import time

#WIFI_STA
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

#ESP_NOW
e = espnow.ESPNow()
e.active(True)

#ESP_MAC
peer = b"0v\xf5\x92'<"
e.add_peer(peer)

#JOYSTICK_1
jx1 = ADC(Pin(34))
jy1 = ADC(Pin(35))
bt1 = Pin(25, Pin.IN, Pin.PULL_UP)

#JOYSTICK_2
jx2 = ADC(Pin(32))
jy2 = ADC(Pin(33))
bt2 = Pin(26, Pin.IN, Pin.PULL_UP)

#DATA_READ
for ADC in [jx1, jy1, jx2, jy2]:
    ADC.atten(ADC.ATTN_11DB)
    
print("_____CONTROLLER ACTIVATE_____")

#LOOP
while True:
    x1 = jx1.read()
    y1 = jy1.read()
    x2 = jx2.read()
    y2 = jy2.read()

    b1 = bt1.value()
    b2 = bt2.value()
    
    data =  "{},{},{},{},{},{}".format(x1, y1, x2, y2, b1, b2)
    
    #DATA_SENDING
    e.send(peer, data)
    
    #Debug
    print(data)

    time.sleep(0.05)