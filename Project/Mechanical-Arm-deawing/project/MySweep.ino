/* Sweep
  by BARRAGAN <http://barraganstudio.com>
  This example code is in the public domain.

  modified 8 Nov 2013
  by Scott Fitzgerald
  https://www.arduino.cc/en/Tutorial/LibraryExamples/Sweep
*/

#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards


void setup() {
  Serial.begin(9600);
  myservo.attach(7);  // attaches the servo on pin 9 to the servo object
  myservo.write(0);              // tell servo to go to position in variable 'pos'
    delay(15);         
}

void loop() {
  if (Serial.available() > 0) {
    // read the incoming string:
    String incomingString = Serial.readStringUntil('\n');

    int deg = (incomingString.substring(0)).toInt();
    Serial.println(deg);
    myservo.write(deg);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15 ms for the servo to reach the position

  }
}
