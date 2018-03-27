// This code is used by Arduino Mega that is connected to Dallas temperature sensor and 
// LCD screen. Before any data is send, any message has to be send to Arduino's Serial.
// After that, the JSON data is send to Serial, that can be read with e.g. Python program.

// Libraries
#include <LiquidCrystal.h>      // LCD
#include <OneWire.h>            // OneWire
#include <DallasTemperature.h>  // Dallas temperature sensor
#include <ArduinoJson.h>        // For making JSON documents

#define ONE_WIRE_BUS_1 40          // Data wire is plugged into port 2 on the Arduino
OneWire oneWire_1(ONE_WIRE_BUS_1); // Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)

DallasTemperature sensors_1(&oneWire_1); // Pass our oneWire reference to Dallas Temperature. 

//                RS  E   D4  D5  D6  D7
LiquidCrystal lcd(37, 36, 35, 34, 33, 32);

// Data variables
float voltageV1,     // Used to store voltage V1
      voltageV2,     // Used to store voltage V2
      temperature1;  // Used to store temperature
char JSON_Data[200]; // Used to store the generated data in JSON

void setup()
{
  Serial.begin(9600);  // Open serial communications.
  sensors_1.begin();   // Start Dallas temperature sensor
  lcd.begin(20, 4);    // Set up the LCD's number of columns: 20 and rows: 4
}

void loop()
{
  // Send data only when you receive data (i.e. command) from client.
  if (Serial.available() > 0) {
      workflow();
      Serial.flush();
  }
}

// Prints the information on LCD
void print_measurement(void)
{
  lcd.setCursor(0,0);
  lcd.print("SeAMK IoTTi");
  
  lcd.setCursor(0,1);
  lcd.print("Voltage V1 =");
  lcd.setCursor(13,1); lcd.print(voltageV1,2);lcd.print(" V");
  
  lcd.setCursor(0,2);
  lcd.print("Voltage V2 =");
  
  lcd.setCursor(13,2); lcd.print(voltageV2,2);lcd.print(" V");
  
  lcd.setCursor(0,3);
  lcd.print("Temperature =");
  lcd.setCursor(13,3); lcd.print(temperature1,2);lcd.print(" C");
}

// Measures all the values available to us (at least those that I know of)
void measure(void)
{
  sensors_1.requestTemperatures(); // Get temperature from Dallas sensor
  
  voltageV1 = analogRead(A0);       // Get the voltage on analog pin
  voltageV1 = voltageV1*10.0/1024;
  
  voltageV2 = analogRead(A1);      // Get the voltage on analog pin
  voltageV2 = voltageV2*10.0/1024; 
    
  temperature1=sensors_1.getTempCByIndex(0); // Save the temperature value on global variable
}

// Send data with MQTT to IBM Cloud IoT platform
void send_data(void)
{
  createJSON(); // Set up the data to be sent
  
  // Send data through serial to the client
  Serial.println(JSON_Data); // Note: needs to be Serial.println !!! In the client (one running the python code), 
                             // it is used as a way to determine when there is no more data to be sent.
}

// A human and Arduino friendly way to create JSON documents in Arduino
void createJSON(void)
{
  StaticJsonBuffer<200> jsonBuffer; // Allocate JSON buffer with 200-byte pool
  
  JsonObject& rootJsonObject = jsonBuffer.createObject();
  JsonObject& nestedJsonObject_STATE = rootJsonObject.createNestedObject("state"); // create JSON object state - required by AWS
  JsonObject& nestedJsonObject_DESIRED = nestedJsonObject_STATE.createNestedObject("desired"); // create JSON object desired, under state - required by AWS

  // Add following data to object desired
  nestedJsonObject_DESIRED["sensor"] = "Dallas"; // Create JSON object named "Sensor", assigned with the name of our sensor
  nestedJsonObject_DESIRED["temperature"] = temperature1; // Create JSON object named "Temperature", assigned with our temperature data 
  
  JsonArray& nestedJsonArray_VOLTAGE = nestedJsonObject_DESIRED.createNestedArray("voltage"); // Creates an array of data with name Voltage
  nestedJsonArray_VOLTAGE.add(voltageV1); // Add V1 to the array
  nestedJsonArray_VOLTAGE.add(voltageV2); // Add V2 to the array
  
  rootJsonObject.printTo(JSON_Data);
}

// The order of methods to handle data
void workflow(void)
{
  measure();           // First measure and save the data
  print_measurement(); // Print them on the LCD screen
  send_data();         // Publish data to AWS
}
