#!/usr/bin/python3

import os
import time
import config
import mail


### FUNCTIONS ###

def read_temperature():
    t = os.popen("/opt/vc/bin/vcgencmd measure_temp").readline()
    t = t.replace("temp=", "")
    t = t.replace("\'C", "")
    return float(t)

def get_hostname():
    hostname = os.popen("hostname").readline()
    return hostname.replace("\n", "")

def send_email(email_from, email_to, subject, temp):
    host_name = get_hostname()
    try:
        os.system("echo \"The temperature of " + host_name + " is " + str(temp) + "\'C\" | mail -s \"" + host_name + " " + subject + "\" -r " + email_from + " " + email_to)
    except:
        pass


### MAIN ###

temp_ok = True
i = config.MON_INTERVAL + 1

while True:

    temp = read_temperature()

    if temp > config.TEMP_CRITICAL:
        send_email(mail.FROM, mail.TO, mail.TEMP_CRITICAL, temp)
        os.system("sudo shutdown -h now")
        exit(0)

    if i > config.MON_INTERVAL:
        if temp > config.TEMP_THRESHOLD:
            if temp_ok:
                temp_ok = False
                send_email(mail.FROM, mail.TO , mail.TEMP_HIGH, temp)
                i = 1
        else:
            if not temp_ok:
                temp_ok = True
                send_email(mail.FROM, mail.TO, mail.TEMP_NORMAL, temp)
                i = 1

    i += 1
    time.sleep(config.MON_PERIOD)
