# Use Amazon's basicShadowUpdater.py sample to test the AWS connection
# Original code at https://github.com/aws/aws-iot-device-sdk-python/blob/master/samples/basicShadow/basicShadowUpdater.py

import time
import serial
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
from callbacks import AWS_ShadowCallback_Update, customShadowCallback_Delete
from AWS_details import LoginDetails as details # Separate place to store login details in.

# Create an AWS IoT MQTT Client using TLSv1.2 Mutual Authentication
myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(details["appName"])
myAWSIoTMQTTShadowClient.configureEndpoint(details["hostname"], details["port"])
myAWSIoTMQTTShadowClient.configureCredentials(details["rootCertificate"], 
                                              details["privateKey"], 
                                              details["certificate"])

# AWS IoT MQTT Client connection configuration
myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

myAWSIoTMQTTShadowClient.connect() # Connect to AWS IoT

deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(details["thingName"], True)

# Delete shadow JSON doc. 
# Note: If there is no data to be deleted, it will be rejected (doesn't crash/stop the program)
deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5)

# Update shadow in a loop
loopCount = 0
while True:
    JSONPayload = '{"state":{"desired":{"property":' + str(loopCount) + '}}}'
    deviceShadowHandler.shadowUpdate(JSONPayload, AWS_ShadowCallback_Update, 5)
    loopCount += 1
    time.sleep(3)