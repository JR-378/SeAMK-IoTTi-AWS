import json

# Insert the name fields of your JSON data into the following array.
# They are used to dynamically print the sent data in customShadowCallback_Update method.
dataNames = ["sensor", "temperature", "voltage"]

# Custom Shadow callback
def customShadowCallback_Update(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")
    if responseStatus == "accepted":
        payloadDict = json.loads(payload)
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Update request with token: " + token + " accepted!")

        # for dynamically printing sent JSON data.
        for i in range(0,len(dataNames)):
            print(dataNames[i] + ": " + str(payloadDict["state"]["desired"][dataNames[i]]))
        
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
        
# for test_AWS_connection.py
def AWS_ShadowCallback_Update(payload, responseStatus, token):
    singleName = ["property"]
    # payload is a JSON string ready to be parsed using json.loads(...)
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")
    if responseStatus == "accepted":
        payloadDict = json.loads(payload)
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Update request with token: " + token + " accepted!")

        # for dynamically printing sent JSON data.
        for i in range(0,len(singleName)):
            print(singleName[i] + ": " + str(payloadDict["state"]["desired"][singleName[i]]))
        
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Update request " + token + " rejected!")