# SeAMK-IoTTi-AWS

## Introduction
This project uses TAMK's Sensor Board, which consists of Arduino Mega 2560, Arduino Ethernet Shield V1 (not used in this example), Dallas temperature sensor and an LCD screen. The data is sent to a computer using serial connection and then sent to the AWS IoT using their Python SDK. As to why we are using Python in between, instead of sending data straight from Arduino, is because Amazon Web Services is too secure for the board to handle the authentication process.

## Quick instructions

1. Upload the JSON-To-PC.ino to your board
2. In Python folder, add your certificate and private key to login folder and modify the AWS details in AWS_details.py to match your AWS IoT service. Mainly the following details:
```Python
rootCertificatePath = loginFolder + "rootCertificate.pem"
privateKeyPath = loginFolder + "MyThermometer001.private.key"
certificatePath = loginFolder + "MyThermometer001.cert.pem"

hostname = "xxxxx.iot.eu-west-2.amazonaws.com" # Your API endpoint.
thingName = "MyThermometer001" # Name of your thing (i.e. device) on AWS
```
3. Run __main__.py to get data from Arduino and send it to AWS IoT.

A more thorough documentation will be in the Docs folder, once it is ready.
