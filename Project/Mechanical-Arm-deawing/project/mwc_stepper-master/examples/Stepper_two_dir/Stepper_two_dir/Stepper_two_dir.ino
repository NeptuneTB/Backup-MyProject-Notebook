#include <avr/wdt.h>  


/**
 * สร้างฟังก์ชันสำหรับหยุดการทำงานหลอก watchdog ให้คิดว่าโปรแกรมค้าง
 * เมื่อเกิน 15MS จะสั่งรีเซ็ตตัวเองอัตโนมัติ
 */
void ArduinoReset()
{
  wdt_enable(WDTO_15MS);
  while (1)
  {
  }
}
void setup() {
  Serial.begin(9600);
  Serial.println("Welcome to ArduinoNa.com. We restart Arduino board soon.");
  delay(2000);
}

void loop() {
  Serial.println("This msg should print once.");
  delay(5000);
  ArduinoReset();
  Serial.println("This msg should not print.");
}