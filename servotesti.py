import MySQLdb
import RPi.GPIO as GPIO
from time import sleep
db = MySQLdb.connect(host="stulinux53.ipt.oamk.fi",
                    user="ryhma3",
                    passwd="meolemmeryhma3",
                    db="codeigniter")
                    
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
servo = 17
PIR = 27
GPIO.setup(servo, GPIO.OUT)
GPIO.setup(PIR, GPIO.IN)
pwm=GPIO.PWM(servo, 50)
pwm.start(0)
x = 0
hiiriHavaittu = 1 

def setAngle(angle):
    duty = angle / 20 + 2
    GPIO.output(servo, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(servo, False)
    pwm.ChangeDutyCycle(0)
    
    
    
try:
    while(1):
        if GPIO.input(PIR):
            print("ok")
            setAngle(90)
            
        else:
            setAngle(0)
        
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()