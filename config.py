
# wifi configuration
WIFI_SSID = 'xxx' #Wifi's SSID
WIFI_PASS = 'xxx' #Wifi's Password

# AWS general configuration
AWS_PORT = 8883
AWS_HOST = 'xxx' #Enpoint Address
AWS_ROOT_CA = '/flash/cert/xxx' #Amazon Root Certificate
AWS_CLIENT_CERT = '/flash/cert/xxx' #User's Certificate
AWS_PRIVATE_KEY = '/flash/cert/xxx' #User's Private Key


################## Subscribe / Publish client #################
CLIENT_ID = 'xxx' #ID for the Publisher / Subscriber
TOPIC = 'xxx' #Topic to Pub / Sub
OFFLINE_QUEUE_SIZE = -1
DRAINING_FREQ = 2
CONN_DISCONN_TIMEOUT = 10
MQTT_OPER_TIMEOUT = 5
LAST_WILL_TOPIC = 'xxx' #Topic to Pub / Sub
LAST_WILL_MSG = 'To All: Last will message'

####################### Shadow updater ########################
####################### Shadow Echo ########################
THING_NAME_2 = "xxx" #Name for the shadow
CLIENT_ID_2 = "Shadow"
CONN_DISCONN_TIMEOUT = 10
MQTT_OPER_TIMEOUT = 5
