# SeAMK-IoTTi-AWS

## Introduction
This project uses TAMK's Sensor Board, which consists of Arduino Mega 2560, Arduino Ethernet Shield V1 (not used in this example), Dallas temperature sensor and an LCD screen. The data is sent to a computer using serial connection and then sent to the AWS IoT using their Python SDK. As to why we are using Python in between, instead of sending data straight from Arduino, is because Amazon Web Services is too secure for the board to handle the authentication process.

## Quick instructions

1. Upload the Arduino-Mega-JSON-To-PC.ino to your board
2. In Python folder, add your certificate and private key to login folder and modify the AWS details in __main__.py to match your AWS IoT.
3. Run __main__.py to get and send the data.

A more thorough documentation will be in the Docs folder, once it is ready.
