# Use Amazon's basicShadowUpdater.py sample to test the AWS connection
# Original code at https://github.com/aws/aws-iot-device-sdk-python/blob/master/samples/basicShadow/basicShadowUpdater.py

# Note: For security reasons private keys and certificates have been deleted from the login folder and
# API endpoint name is replaced with xxxxx

import time
import serial
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

# Custom Shadow callback
def customShadowCallback_Update(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")
    if responseStatus == "accepted":
        payloadDict = json.loads(payload)
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Update request with token: " + token + " accepted!")
        print("property: " + str(payloadDict["state"]["desired"]["property"]))
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Update request " + token + " rejected!")

def customShadowCallback_Delete(payload, responseStatus, token):
    if responseStatus == "timeout":
        print("Delete request " + token + " time out!")
    if responseStatus == "accepted":
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Delete request with token: " + token + " accepted!")
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Delete request " + token + " rejected!")

# ******************************************** AWS details ******************************************** #
# root and device certificate, alongside with device private key should be put into the login folder
loginFolder = "login/"

# Paths to the certificates, rename the certificates accordingly. 
# Note: Make sure there is no spaces in the name
rootCertificatePath = loginFolder + "rootCertificate.pem"
privateKeyPath = loginFolder + "MyThermometer001.private.key"
certificatePath = loginFolder + "MyThermometer001.cert.pem"

appName = "testIoTPySDK" # Name of the app, can be anything.
hostname = "xxxxx.iot.eu-west-2.amazonaws.com" # Your API endpoint.
port = 8883 # 8883 when connecting with MQTT, 8443 for HTTP, 443 for WebSocket and HTTP.
thingName = "MyThermometer001" # Name of your thing (i.e. device) on AWS
topicToPublish = "$aws/things/" + thingName + "/shadow/update"
# **************************************************************************************************** #

# Create an AWS IoT MQTT Client using TLSv1.2 Mutual Authentication
myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(appName)
myAWSIoTMQTTShadowClient.configureEndpoint(hostname, port)
myAWSIoTMQTTShadowClient.configureCredentials(rootCertificatePath, privateKeyPath, certificatePath)

# AWS IoT MQTT Client connection configuration
myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

myAWSIoTMQTTShadowClient.connect() # Connect to AWS IoT

deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingName, True)

# Delete shadow JSON doc. 
# Note: If there is no data to be deleted, it will be rejected (doesn't crash/stop the program)
deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5)

# Update shadow in a loop
loopCount = 0
while True:
    JSONPayload = '{"state":{"desired":{"property":' + str(loopCount) + '}}}'
    deviceShadowHandler.shadowUpdate(JSONPayload, customShadowCallback_Update, 5)
    loopCount += 1
    time.sleep(3)