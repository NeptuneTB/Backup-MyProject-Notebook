#include <Servo.h>
#define PIN_7 7  // gpio16 = D0
#define PIN_8 8  // gpio5 = D1
#define PIN_9 9  // gpio4 = D2
#define PIN_10 10  // gpio0 = D3

Servo myservo1, myservo2, myservo3, myservo4;
int c;

int sv1 = 0;
int sv2 = 0;
int sv3 = 0;
int sv4 = 0;

int ori_sv1 = 88;
int ori_sv2 = 115;
int ori_sv3 = 90;
int ori_sv4 = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(1000000);
  myservo1.attach(PIN_7);
  myservo2.attach(PIN_8);
  myservo3.attach(PIN_9);
  myservo4.attach(PIN_10);
  //ควบคุมด้านบน s1,s3
  //ควบคุมขวา s1,s2 
  myservo1.write(90);
  myservo2.write(90); 
  //ควบคุมด้านล่าง s2,s4
  //ควบคุมซ้าย s3,s4
  myservo3.write(90);
  myservo4.write(90); 

  //  for (int i = 0; i <= 90; i++) {
  //    myservo1.write(i);
  //    delay(25);
  //  }
  //  for (int i = 0; i <= 0; i++) {
  //    myservo2.write(i);
  //    delay(10);
  //  }
  //  for (int i = 0; i <= 0; i++) {
  //    myservo3.write(i);
  //    delay(10);
  //  }
  //  for (int i = 0; i <= 70; i++) {
  //    myservo4.write(i);
  //    delay(25);
  //  }
}

void loop() {
  int cnt = 0;
  String str = "";
  // put your main code here, to run repeatedly:
  while (Serial.available() > 0) //Checks is there any data in buffer
  {
    //str += char(Serial.read());
    str = Serial.readStringUntil('\n');
    cnt++;
  }
  if (cnt != 0) {
    //Serial.println(str);
    //String c = str.substring(0,2);
    String c = str.substring(0, 1);
    //Serial.println(c);
    if (c[0] == 'M') {
      //Serial.println(c[0]);
      String m = str.substring(1, 2);
      int M = m.toInt();
      if (M == 1) {
        //Serial.println(M);
        // S = myservo1;
        chkAngle(str, myservo1);
        Serial.println("servo1"); 

      }
      else if (M == 2) {
        //S = myservo2;
        chkAngle(str, myservo2);
        Serial.println("servo2");
      }
      else if (M == 3) {
        //S = myservo3;
        chkAngle(str, myservo3);
        Serial.println("servo3");
      }
      else if (M == 4) {
        //S = myservo4;
        chkAngle(str, myservo4);
        Serial.println("servo4");
      }

      //Serial.println(m);
      //      String a = str.substring(3);
      //      int A = a.toInt();
      //      int C = c.toInt();
      //      Serial.println(c);
      //      String r = str.substring(3,6);
      //      int R = r.toInt();

      //      numservo(S,R);
    }
  }
}

void chkAngle(String str, Servo S) {
  String c = str.substring(2, 3);
  if (c[0] == 'A') {
    String a = str.substring(3);
    int A = a.toInt();
    numservo(S, A);
  }


}

void numservo(Servo servo_num, int value) {
  sv1 = value;
  int s = abs(ori_sv1 - sv1);
  int n = 1;
  while (sv1 < ori_sv1) {
    servo_num.write(ori_sv1);
    //Serial.println(ori_sv1);
    ori_sv1 = ori_sv1 - 1;
    delay(10);
    n++;
  }
  while (sv1 > ori_sv1) {
    servo_num.write(ori_sv1);
    //Serial.println(ori_sv1);
    ori_sv1 = ori_sv1 + 1;
    delay(10);
    n++;
  }
  Serial.println(ori_sv1);
}

//    sv2 = value;
//    int s = abs(ori_sv2 - sv2);
//    int n = 1;
//    while (sv2 < ori_sv2) {
//      servo_num.write(ori_sv2);
//      //Serial.println(ori_sv2);
//      ori_sv2 = ori_sv2 - 1;
//      delay(10);
//      n++;
//    }
//    while (sv2 > ori_sv2) {
//      servo_num.write(ori_sv2);
//      //Serial.println(ori_sv2);
//      ori_sv2 = ori_sv2 + 3;
//      delay(10);
//      n++;
//    }
//    Serial.println(ori_sv2);
//  }
//
//    sv3 = value;
//    int s = abs(ori_sv3 - sv3);
//    int n = 1;
//    while (sv3 < ori_sv3) {
//      servo_num.write(ori_sv3);
//      //Serial.println(ori_sv3);
//      ori_sv3 = ori_sv3 - 1;
//      delay(10);
//      n++;
//    }
//    while (sv3 > ori_sv3) {
//      servo_num.write(ori_sv3);
//      //Serial.println(ori_sv3);
//      ori_sv3 = ori_sv3 + 1;
//      delay(10);
//      n++;
//    }
//    Serial.println(ori_sv3);
//  }
//
//    sv4 = value;
//    int s = abs(ori_sv1 - sv1);
//    int n = 1;
//    while (sv4 < ori_sv4) {
//      servo_num.write(ori_sv4);
//      //Serial.println(ori_sv4);
//      ori_sv4 = ori_sv4 - 1;
//      delay(10);
//      n++;
//    }
//    while (sv4 > ori_sv4) {
//      servo_num.write(ori_sv4);
//      //Serial.println(ori_sv4);
//      ori_sv4 = ori_sv4 + 1;
//      delay(10);
//      n++;
//    }
//    Serial.println(ori_sv4);
//  }
