# pysense-aws
Code for Uploading Pysense sensor data to AWS IoT Core

First you need the add the next libraries to the /lib folder (besides the one for the sensors)

https://github.com/pycom/aws-pycom/tree/master/AWSIoTPythonSDK

This code uploads the sensor data to the cloud and also updates the shadow

There are 3 scripts: boot.py, main.py and config.py

boot.py is the first script run and it's used to set up the wifi connection

main.py is then run with the main sensor function. It uses values and data contained on the file config.py
