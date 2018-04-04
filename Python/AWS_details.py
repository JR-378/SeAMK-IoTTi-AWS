""" AWS login details, modify according to your IoT service

 Note: For security reasons private key and certificate have been deleted from the login folder and
 API endpoint name is replaced with xxxxx """

# root and device certificate, alongside with device private key should be put into the login folder
loginFolder = "login/"

# Paths to the certificates, rename the certificates accordingly. 
# Note: Make sure there is no spaces in the name of the file
rootCertificatePath = loginFolder + "rootCertificate.pem"
privateKeyPath = loginFolder + "MyThermometer001.private.key"
certificatePath = loginFolder + "MyThermometer001.cert.pem"

appName = "testIoTPySDK" # Name of the app, can be anything.
hostname = "xxxxx.iot.eu-west-2.amazonaws.com" # Your API endpoint.
port = 8883 # 8883 when connecting with MQTT, 8443 for HTTP, 443 for WebSocket and HTTP.
thingName = "MyThermometer001" # Name of your thing (i.e. device) on AWS

LoginDetails = {
    "appName": appName,
    "hostname": hostname,
    "port": port,
    "thingName": thingName,
    "rootCertificate": rootCertificatePath,
    "privateKey": privateKeyPath,
    "certificate": certificatePath
}