""" This code is used to retrieve data from Arduino Mega that is connected through serial port and the data
 itself is being sent to Amazon Web Services (AWS) Internet of Things (IoT) service. As the data is 
 sent in JSON format (using ArduinoJson) all we have to do is make sure that it is in the correct format 
 for the AWS IoT Python SDK. The data is being sent every minute and during waiting the port is closed.
 
 If you don't have an Arduino to sent data with, use test_AWS_connection.py to simply test your IoT service,

 Note: Edit AWS_details.py to match your IoT service.

 Note 2: Edit callbacks.py - dataNames variable if your data is in different format. It is used to define
 the objects in your JSON document, that will be printed on console after each succesful update. """

import time
import serial
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
from callbacks import customShadowCallback_Update, customShadowCallback_Delete # Import the required callbacks
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


def main():
    """ Get data from Arduino and sent it to AWS IoT """
    
    # Establish serial connection.
    try:
        arduinoSerial = serial.Serial("COM5", timeout=1, baudrate=9600)
    except:
        print("Unable to establish serial connection with Arduino. Check the port.")
    
    time.sleep(2) # Give time for arduino to wake up.

    # Keep looping while the port is open.
    while arduinoSerial.isOpen():
        arduinoSerial.write(1) # Tell Arduino to send data.
        JSON_Data = arduinoSerial.readline().strip() # Get the data from arduino serial
        # As the data is in bytes, next we make sure it is in the right format and upload the data to AWS
        for data in JSON_Data.decode('utf-8').split('\n'): 
            deviceShadowHandler.shadowUpdate(str(data), customShadowCallback_Update, 5)
        arduinoSerial.close() # Close the port
        time.sleep(58) # Wait for 58 seconds before uploading again

        try:
            arduinoSerial.open() # Open the port again.
        except:
            print("Unable to open port.")
        time.sleep(2) # Give time for arduino to wake up.
        

if __name__ == "__main__":
    main()