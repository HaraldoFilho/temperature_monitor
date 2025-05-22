#!/usr/bin/python3

import os
import time
import config
import mail

from datetime import datetime


### FUNCTIONS ###

def read_temperature():
    t = os.popen("vcgencmd measure_temp").readline()
    t = t.replace("temp=", "")
    t = t.replace("\'C", "")
    return float(t)

def get_hostname():
    hostname = os.popen("hostname").readline()
    return hostname.replace("\n", "")

def write_log(temp, level):
    now = datetime.now()
    log = open("/home/pi/temperature_monitor/temp_mon.log", "a")
    log.write("[" + datetime.strftime(now, "%d/%m/%y %H:%M:%S") + "] " + str(temp) + " : " + level + "\n")
    log.close

def send_email(email_from, email_to, subject, temp):
    host_name = get_hostname()
    try:
        os.system("echo \"Device temperature is " + str(temp) + "\'C\" | mail -s \"" + subject + "\" -A \"/home/pi/temperature_monitor/temp_mon.log\" -a From:" + host_name + "\<" + email_from + "\> " + email_to)
    except:
        pass


### MAIN ###

temp_ok = True
i = config.MON_INTERVAL + 1

while True:

    temp = read_temperature()

    if temp > config.TEMP_CRITICAL:
        write_log(temp, "CRITICAL")
        send_email(mail.FROM, mail.TO, mail.TEMP_CRITICAL, temp)
        os.system("sudo shutdown -h now")
        exit(0)

    if i > config.MON_INTERVAL:
        if temp > config.TEMP_HIGH:
            if temp_ok:
                temp_ok = False
                write_log(temp, "HIGH")
                send_email(mail.FROM, mail.TO , mail.TEMP_HIGH, temp)
                i = 1
        else:
            if not temp_ok:
                temp_ok = True
                write_log(temp, "NORMAL")
                send_email(mail.FROM, mail.TO, mail.TEMP_NORMAL, temp)
                i = 1

    i += 1
    time.sleep(config.MON_PERIOD)
