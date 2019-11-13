import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
servo = 17
GPIO.setup(servo, GPIO.OUT)
pwm=GPIO.PWM(servo, 50)
pwm.start(1)
#x = input ()
x = 90
hiiriHavaittu = 1
def setAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(servo, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(servo, False)
    pwm.ChangeDutyCycle(0)
    
    setAngle(x)


pwm.stop()
GPIO.cleanup()
