#!/bin/bash

cp files/mail mail.py
sudo cp files/temp-mon /etc/init.d/
sudo update-rc.d temp-mon defaults
sudo visudo

