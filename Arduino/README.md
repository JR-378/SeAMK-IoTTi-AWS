# Arduino

libraries.zip contains the required libraries for the code. Unzip it with 7-Zip or Winrar and Copy and paste the folders inside into the Arduino libraries folder, usually located in C:\Users\YOUR-USERNAME\Documents\Arduino\libraries

For information on installing libraries, see: http://www.arduino.cc/en/Guide/Libraries

If you have a Chinese copy of Arduino Mega 2560, Driver.zip contains the USB drivers for the PC.

## JSON-To-PC.ino

Used to send data to serial in JSON format.

## I don't have Dallas temperature sensor, nor an LCD screen

Remove methods:

```C++
void print_measurement(void)
{
  // Code
}
void measure(void)
{
  // Code
}
```

Remember to remove the methods from `void workflow(void)` as well, and create a JSON document with hard-coded data.
