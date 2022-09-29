#include <arduino-timer.h>
#define enableR 10

int value = 0;
auto timer1 = timer_create_default(); // create a timer with default settings

float kp = 0.0;
float ki = 0.0;
float kd = 0.0;

float ticks_per_tour = 230.0;

float actual_distance = 0;
float command = 1.0; 
float error = 0 ;

long ticks_done = 0;

int pwm = 0;
float voltage = 0;

bool callback1(void *) {

    actual_distance = ticks_done / ticks_per_tour;

    error = command - actual_distance;

    voltage = kp * error;

    if ( voltage > 8.0 )
      voltage = 8.0;

    else if ( voltage < 0.0 )
      voltage = 0.0;

    pwm = (int) ( (voltage * 255) / 12.0 );
    analogWrite(enableR, pwm);
    Serial.println(actual_distance);
     
  return true; // repeat? true
}

void Count() {
  ticks_done++; 
}
void setup() {
    Serial.begin(115200);
  // initialize the LED pin as an output:

    pinMode(13, OUTPUT);
    timer1.every(5, callback1);
    attachInterrupt(digitalPinToInterrupt(2), Count, RISING);
}

void loop() {
 while((kp <= 0.0 ))
 {
  kp =  ( Serial.read());
  //ki = Serial.read();
  //kd = Serial.read();
  kp = kp / 10.0;
 }

 
digitalWrite(13,HIGH);


 timer1.tick(); 
}
