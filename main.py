# main.py -- put your code here!
#!/usr/bin/env python
#
# Copyright (c) 2020, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

# See https://docs.pycom.io for more information regarding library specifics

import time
import pycom
import config
import machine
import json
from MQTTLib import AWSIoTMQTTClient
from MQTTLib import AWSIoTMQTTShadowClient
from network import WLAN
from pycoproc_1 import Pycoproc
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

pycom.heartbeat(False)

pycom.rgbled(0x7f7f00) #Yellow for configuring

Custom Shadow callback with echo
class shadowCallbackContainer:
	def __init__(self, deviceShadowInstance):
		self.deviceShadowInstance = deviceShadowInstance

	# Custom Shadow callback
	def customShadowCallback_Delta(self, payload, responseStatus, token):
		print("Received a delta message:")
		payloadDict = json.loads(payload)
		deltaMessage = json.dumps(payloadDict["state"])
		print(deltaMessage)
		print("Request to update the reported state...")
		newPayload = '{"state":{"reported":' + deltaMessage + '}}'
		self.deviceShadowInstance.shadowUpdate(newPayload, None, 5)
		print("Sent.")


# user specified callback functions
def customShadowCallback_Update(payload, responseStatus, token):
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")
    if responseStatus == "accepted":
        payloadDict = json.loads(payload)
        print("Update request with token: " + token + " accepted!")
        print("property: " + str(payloadDict["state"]["desired"]["property"]))
    if responseStatus == "rejected":
        print("Update request " + token + " rejected!")

def customShadowCallback_Delete(payload, responseStatus, token):
    if responseStatus == "timeout":
        print("Delete request " + token + " time out!")
    if responseStatus == "accepted":
        print("Delete request with token: " + token + " accepted!")
    if responseStatus == "rejected":
        print("Delete request " + token + " rejected!")


# configure the MQTT clients
pycomAwsMQTTClient = AWSIoTMQTTClient(config.CLIENT_ID)
pycomAwsMQTTClient.configureEndpoint(config.AWS_HOST, config.AWS_PORT)
pycomAwsMQTTClient.configureCredentials(config.AWS_ROOT_CA, config.AWS_PRIVATE_KEY, config.AWS_CLIENT_CERT)
pycomAwsMQTTClient.configureOfflinePublishQueueing(config.OFFLINE_QUEUE_SIZE)
pycomAwsMQTTClient.configureDrainingFrequency(config.DRAINING_FREQ)
pycomAwsMQTTClient.configureConnectDisconnectTimeout(config.CONN_DISCONN_TIMEOUT)
pycomAwsMQTTClient.configureMQTTOperationTimeout(config.MQTT_OPER_TIMEOUT)
pycomAwsMQTTClient.configureLastWill(config.LAST_WILL_TOPIC, config.LAST_WILL_MSG, 1)


pycomAwsMQTTShadowClient = AWSIoTMQTTShadowClient(config.CLIENT_ID_2)
pycomAwsMQTTShadowClient.configureEndpoint(config.AWS_HOST, config.AWS_PORT)
pycomAwsMQTTShadowClient.configureCredentials(config.AWS_ROOT_CA, config.AWS_PRIVATE_KEY, config.AWS_CLIENT_CERT)
pycomAwsMQTTShadowClient.configureConnectDisconnectTimeout(config.CONN_DISCONN_TIMEOUT)
pycomAwsMQTTShadowClient.configureMQTTOperationTimeout(config.MQTT_OPER_TIMEOUT)



#Connect to MQTT Host
if pycomAwsMQTTClient.connect():
    print('AWS connection succeeded')
else:
	print('No connection to AWS')
	machine.reset()
	
if pycomAwsMQTTShadowClient.connect():
    print('AWS Shadow Client connection succeeded')
else:
    print('No connection to AWS Shadow Client')
		


deviceShadowHandler = pycomAwsMQTTShadowClient.createShadowHandlerWithName(config.THING_NAME_2, True)

shadowCallbackContainer_Bot = shadowCallbackContainer(deviceShadowHandler)
deviceShadowHandler.shadowRegisterDeltaCallback(shadowCallbackContainer_Bot.customShadowCallback_Delta)

# Delete shadow JSON doc
deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5)

# Send message to host

py = Pycoproc(Pycoproc.PYSENSE)


while True:

	
	pycom.rgbled(0x007f00) # green for working

	msg = {}
    
	si = SI7006A20(py)
	msg["Temperature"] = round(si.temperature(),2)
	msg["Humidity"] = si.humidity()
	msg["DewPoint"] = si.dew_point()
	
	alt = MPL3115A2(py,mode=ALTITUDE)
	msg["Altitude"] = alt.altitude()

	press = MPL3115A2(py,mode=PRESSURE)
	msg["Pressure"] = press.pressure()

	li = LTR329ALS01(py)
	msg["Light"] = li.lux()
	
	acc = LIS2HH12(py)
	msg["Acceleration"] = acc.acceleration()
	msg["Roll"] = acc.roll()
	msg["Pitch"] = acc.pitch()
	
	msg["Battery"] = py.read_battery_voltage()
	
	message = json.dumps(msg)

	print(message)
	
	print("----------------------------------------------------------------------")
	
	
	if wlan.isconnected():
		pycomAwsMQTTClient.publish(config.TOPIC, message, 1)
		time.sleep(5.0)
		JSONPayload = '{"state":{"desired":{"property":' + message + '}}}'
		deviceShadowHandler.shadowUpdate(JSONPayload, customShadowCallback_Update, 5)
	else:
		machine.reset()

	

	for cycles in range(60): # stop after 1 min
		pycom.rgbled(0x7f0000) # red
		time.sleep(3)
		pycom.rgbled(0x0A0A08) # white
		time.sleep(2)
