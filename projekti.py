import projekti_hiirenTunnistusKuvasta
import mysql.connector
import RPi.GPIO as GPIO
import time
import requests
from picamera import PiCamera

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
TRIGGER = 18
ECHO = 23
servo2 = 22
servo = 17
IR = 27

#set GPIO direction (IN / OUT)
GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(servo, GPIO.OUT)
GPIO.setup(servo2, GPIO.OUT)
GPIO.setup(IR, GPIO.IN)

pwm=GPIO.PWM(servo, 50)
pwm.start(0)
pwm2=GPIO.PWM(servo2, 50)
pwm2.start(0)

def takePhoto():
    timestr = time.strftime("%Y%m%d-%H%M%S")
    imageFileName = "img-"+timestr+".jpg"
    # PiCamv2 initialization  
    camera = PiCamera()
    camera.resolution = (720, 480)
    # capture image
    camera.capture('/home/pi/tensorflow1/models/research/object_detection/kuvat/%s' % imageFileName)
    time.sleep(1)
    camera.close()
    return imageFileName
    
def sendPhotoToWeb(imgName):
    url = "http://stulinux53.ipt.oamk.fi/codeigniter/application/models/photoUpload.php/"
    # send file to server
    files = {'file': open('/home/pi/tensorflow1/models/research/object_detection/kuvat/%s' % imgName, 'rb')}
    rq = requests.post(url,files=files)
    # Wait for 10 milliseconds
    time.sleep(0.01)
    messageBack = "Viimeksi web-palvelimelle lähetetty kuva: " + imgName
    return messageBack

def checkFillFactor():
    # set Trigger to HIGH
    GPIO.output(TRIGGER, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(TRIGGER, False)
    startTime = time.time()
    stopTime = time.time()
    # save StartTime
    while GPIO.input(ECHO) == 0:
        startTime = time.time()
    # save time of arrival
    while GPIO.input(ECHO) == 1:
        stopTime = time.time()
 
    # time difference between start and arrival
    timeElapsed = stopTime - startTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (timeElapsed * 34300) / 2
    
    #print ("Measured Distance = %.1f cm" % distance)
    time.sleep(1)
    fillFactor = 0
    if (distance <= 4):
        fillFactor = 100
    elif (distance <= 9):
        fillFactor = 75
    elif (distance <= 14):
        fillFactor = 50
    elif (distance <= 19):
        fillFactor = 25
    elif (distance >= 22.5):
        fillFactor = 0
    
    #print(fillFactor)
    return fillFactor

def setAngle(angle):
    duty = angle / 20 + 2
    GPIO.output(servo, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo, False)
    pwm.ChangeDutyCycle(0)
    
def setAngle2(angle):
    duty = angle / 20 + 2
    GPIO.output(servo2, True)
    pwm2.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo2, False)
    pwm2.ChangeDutyCycle(0)
        
mouses = 0
fillFactor = 0
idkaappaus = None
 
while(1):
    print("IR tila: ",GPIO.input(IR))
    if GPIO.input(IR):  
        # Close hatch
        setAngle(90)
        # Take picture with timestamp
        image = takePhoto()
        # Send picture taken above to detection-script using tensorflow-model
        mouseDetected = projekti_hiirenTunnistusKuvasta.mouseDetectorFromPicture(image)
        print("tunnistus arvo: ",mouseDetected)
        if (mouseDetected >= 0.7):
          # Open and close bottom hatch
            setAngle2(90)
            time.sleep(1)
            setAngle2(0)
            
            print('hiiret++')
            # Send photo of the captured thing to web
            print(sendPhotoToWeb(image))
            
            # Open mysql-connection
            mydb = mysql.connector.connect(host="stulinux53.ipt.oamk.fi",user="ryhma3",passwd="meolemmeryhma3",database="codeigniter") 
            mycursor = mydb.cursor()
 
          # Update mouse container's fill factor procentage via ultrasonic sensor
            fillFactor = checkFillFactor()
            print("fillfaktori: ", fillFactor)

            sql = "INSERT INTO hiiri VALUES (%s, %s)"
            val = (idkaappaus, fillFactor)
            
            try:
                # Execute the SQL command
                mycursor.execute(sql, val)
                # Commit changes in database
                mydb.commit()
            except mysql.connector.Error as err:
                print("Virhe: {}".format(err))
                
            # Diconnect from the server    
            mydb.close()
            # Open front hatch for a new entrapment
            setAngle(0)
            
        else:
            # If mouse wasn't detected, let wrongfully captured thing out
            setAngle(0)
            print('else')
            