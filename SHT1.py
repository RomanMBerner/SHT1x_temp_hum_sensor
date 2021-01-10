#####################################################
# python script to read the temperature and the     #
# humidity with the SHT1x sensor.                   #
# Last modifications: 17.11.2019 by R.Berner        #
#####################################################

import sched, time
import datetime

import RPi.GPIO as GPIO
import subprocess

from sht1x.Sht1x import Sht1x as SHT1x

#file = open("measured_data.txt", "w")
#file.write("Date and time\t\tT [C]\tLinHum\tCorrHum\tDewPoint [C]\n" )

###s = sched.scheduler(time.time, time.sleep)
###def TakeData(sc):
while True:
    try:
        dataPin = 11
        clkPin = 7

        sht1x = SHT1x(dataPin, clkPin)
        temperature = sht1x.read_temperature_C()
        if(temperature>50):
            print(" temperature = %.2f > 50 deg C -> reject " %temperature)
            continue

        sht1x = SHT1x(dataPin, clkPin)
        rawHumidity = sht1x.read_rawHumidity()
        # Apply linear conversion to raw value
        C1 = -2.0468        # for 12 Bit, taken from Sht1x.py
        C2 =  0.0367        # for 12 Bit, taken from Sht1x.py
        C3 = -0.0000015955  # for 12 Bit, taken from Sht1x.py
        T1 =  0.01          # for 14 Bit @ 5V, taken from Sht1x.py
        T2 =  0.00008       # for 14 Bit @ 5V, taken from Sht1x.py
        linearHumidity = C1 + C2 * rawHumidity + C3 * rawHumidity * rawHumidity
        # Correct humidity value for current temperature
        correctedHumidity = (temperature - 25.0) * (T1 + T2 * rawHumidity) + linearHumidity
        if(correctedHumidity>100):
            correctedHumidity = 100
        if(correctedHumidity<0.1):
            correctedHumidity = 0.1
        dewPoint = sht1x.calculate_dew_point(temperature, correctedHumidity)
        print("temperature [C]: \t{:0.2f}" .format(temperature) )
        #print("raw humidity [int]: \t{}" .format(rawHumidity) )
        #print("linear humidity [%]: \t{:0.2f}" .format(linearHumidity) )
        print("corrected humidity [%]: {:0.2f}" .format(correctedHumidity) )
        #print("dew point [C]: \t\t{:0.2f}" .format(dewPoint) )
        #print("Date: \t\t\t{}" .format(datetime.datetime.now().strftime("%Y-%m-%d")) )
        print("Time: \t\t\t{}" .format(datetime.datetime.now().strftime("%H:%M:%S")) )
        print("---------------------------------------")
        #GPIO.cleanup()

        #file = open("measured_data.txt", "a")
        #file.write("%s\t%0.2f\t%0.2f\t%0.2f\t%0.2f\n" %(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"), temperature, linearHumidity, correctedHumidity, dewPoint) )
        #file.close()

        sensor = 0
        post1 = "temperature,sensor=" + str(sensor) + " value=" + str(temperature)
        post2 = "humidity,sensor=" + str(sensor) + " value=" + str(correctedHumidity)
        post3 = "dewPoint,sensor=" + str(sensor) + " value=" + str(dewPoint)

        subprocess.call(["curl", "-i", "-XPOST", "192.168.1.88:8086/write?db=SHT1_temp_and_hum", "--data-binary", post1])
        subprocess.call(["curl", "-i", "-XPOST", "192.168.1.88:8086/write?db=SHT1_temp_and_hum", "--data-binary", post2])
        subprocess.call(["curl", "-i", "-XPOST", "192.168.1.88:8086/write?db=SHT1_temp_and_hum", "--data-binary", post3])

        time.sleep(1)
    except(ValueError,SystemError):
        print("Excepion! \n Continue ...")
##while True:
    ###s.enter(5, 0, TakeData, (s,))
    ###s.run()
