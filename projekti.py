import pymysql
import RPi.GPIO as GPIO
import hiirenTunnistus_v2
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
servo2 = 22
servo = 17
PIR = 27
GPIO.setup(servo, GPIO.OUT)
GPIO.setup(servo2, GPIO.OUT)
GPIO.setup(PIR, GPIO.IN)
pwm=GPIO.PWM(servo, 50)
pwm.start(0)
pwm2=GPIO.PWM(servo2, 50)
pwm2.start(0)
def openDatabaseConnection():
    db = pymysql.connect("stulinux53.ipt.oamk.fi", "ryhma3", "meolemmeryhma3", "codeigniter") 
    cursor = db.cursor
def setAngle(angle):
    duty = angle / 20 + 2
    GPIO.output(servo, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(servo, False)
    pwm.ChangeDutyCycle(0)
    
def setAngle2(angle):
    duty = angle / 20 + 2
    GPIO.output(servo2, True)
    pwm2.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(servo2, False)
    pwm2.ChangeDutyCycle(0)
        
mouses = 0
fillFactor = 0

try:
    while(1):
        if GPIO.input(PIR):  
            # Close hatch
            setAngle(90)
            #openDatabaseConnection()
            # mouse_detector returns detection confidence procentage in decimal
            mouseDetected = hiirenTunnistus_v2.mouse_detector()
            print(mouseDetected)
            if (mouseDetected >= 0.7):
                print('KUKKUU')
                # Open and close bottom hatch
                setAngle2(90)
                sleep(1)
                setAngle2(0)
                # Update mouse count
                mouses += 1
                print('hiirien lkm', mouses)
            
                
                # Update mouse container's fill factor procentage via ultrasonic sensor
                #checkFillFactor()
                
                sql = """INSERT INTO hiiri (idkaappaus, aika, tayttoaste, idhiiri) VALUES (NULL, NULL, %fillFactor, %mouses)"""
                #try:
                    # Execute the SQL command
                    #cursor.execute(sql)
                    # Commit changes in database
                    #db.commit
                #except:
                    # Rollback in case there is error
                    #db.rollback()
                # Diconnect from the server    
                #db.close()
                
                # Open front hatch for a new entrapment
                setAngle(0)
                
            else:
                # If mouse wasn't detected, let wrongfully captured thing out
                setAngle(0)
            
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()