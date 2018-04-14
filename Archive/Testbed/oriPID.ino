// import libraries 
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <stdlib.h> 
#include <Servo.h>

/*---------------------------------------------*/
// create servo object (esc) and data values

Servo leftEscMotor; // left motor
//Servo rightEscMotor; // right motor

int leftEscPin = 9; // pin conected to esc controlling the leftMotor
//int rightESCPin = 10; // pin connected to esc controlling the rightMotor 
int minPulseRate = 1000; 
int maxPulseRate = 2000;
int throttleChangeDelay = 100;

// default speed of motors (when heading straight, both motors spin at 90)
// range of ESC speed is 0 - 179.  
double defaultSpeed = 89.5;
double leftSpeedPID = 89.5; // PID speed for motor on the left
//double rightSpeedPID = 90; // PID speed for motor on the right 

/*---------------------------------------------*/
// create IMU (BNO055) object and its data values

Adafruit_BNO055 bno = Adafruit_BNO055(55);
#define BNO055_SAMPLERATE_DELAY_MS (100)

double absYawOri = 0.0; // orientation imu should always point to
double currYawOri = 0.0; // the current yaw orientation 

// the difference between desired orientation and current orientation 
double yawDiff = currYawOri - absYawOri; 

long currTime = 0.0; 
/**************************************************************************
    Displays some basic information on BNO055 sensor from the unified
    sensor API sensor_t type (see Adafruit_Sensor for more information)
***************************************************************************/
void displaySensorDetails(void)
{
  sensor_t sensor;
  bno.getSensor(&sensor);
  Serial.println("------------------------------------");
  Serial.print  ("Sensor:       "); Serial.println(sensor.name);
  Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
  Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
  Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" xxx");
  Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" xxx");
  Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" xxx");
  Serial.println("------------------------------------");
  Serial.println("");
  delay(500);
}

/***********************************************************************
    Display some basic info about the sensor status
 ***********************************************************************/
void displaySensorStatus(void)
{
  /* Get the system status values (mostly for debugging purposes) */
  uint8_t system_status, self_test_results, system_error;
  system_status = self_test_results = system_error = 0;
  bno.getSystemStatus(&system_status, &self_test_results, &system_error);

  /* Display the results in the Serial Monitor */
  Serial.println("");
  Serial.print("System Status: 0x");
  Serial.println(system_status, HEX);
  Serial.print("Self Test:     0x");
  Serial.println(self_test_results, HEX);
  Serial.print("System Error:  0x");
  Serial.println(system_error, HEX);
  Serial.println("");
  delay(500);
}

/*********************************************************************
    Display sensor calibration status
 *********************************************************************/
void displayCalStatus(void)
{
  /* Get the four calibration values (0..3) */
  /* Any sensor data reporting 0 should be ignored, */
  /* 3 means 'fully calibrated" */
  uint8_t system, gyro, accel, mag;
  system = gyro = accel = mag = 0;
  bno.getCalibration(&system, &gyro, &accel, &mag);

  /* The data should be ignored until the system calibration is > 0 */
  Serial.print("\t");
  if (!system)
  {
    Serial.print("! ");
  }

  /* Display the individual values */
  Serial.print("Sys:");
  Serial.print(system, DEC);
  Serial.print(" G:");
  Serial.print(gyro, DEC);
  Serial.print(" A:");
  Serial.print(accel, DEC);
  Serial.print(" M:");
  Serial.print(mag, DEC);
}

void setup() {
  Serial.begin(9600);
  /*-------------------------------------------------------*/
  // attach left and right esc with pulse range
  leftEscMotor.attach(leftEscPin, minPulseRate, maxPulseRate); 
  leftEscMotor.write(0); // min value to calibrate/start the ESC

  //rightEscMotor.attach(rightEscPin, minPulseRate, maxPulseRate);
  //rightEscMotor.write(0); 
  /*-------------------------------------------------------*/
  
  // check if BNO055 is connected
  if(!bno.begin())
  {
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
  
  /* Display some basic information on this sensor */
  displaySensorDetails();

  /* Optional: Display current status */
  displaySensorStatus();

  bno.setExtCrystalUse(true);
  /*------------------------------------------------------*/
}

void loop() {
  currTime = millis(); /* get current time of the program */ 
  /* set motor to its default speed when going straight */
  leftEscMotor.write(defaultSpeed); 
  //rightEscMotor.write(defaultSpeed); 
  
  /* Get a new sensor event */
  sensors_event_t event;
  bno.getEvent(&event);

  /* Display the floating point data */
  Serial.print("X: ");
  Serial.print(event.orientation.x, 4); // yaw data 
  /*Serial.print("\tY: ");
  Serial.print(event.orientation.y, 4); // roll data
  Serial.print("\tZ: ");
  Serial.print(event.orientation.z, 4); // pitch data
  /* Optional: Display calibration status */
  //displayCalStatus();

  /* Optional: Display sensor status (debug only) */
  //displaySensorStatus();

  /* New line for the next sample */
  Serial.println("");

  // Take some time at the beginning to update the
  // initial value of the yaw.
  if(currTime - 0 < 3000) {
    currYawOri = event.orientation.x;
  }

  // Wait for 5 seconds after the initial value is recorded.
  if(currTime - 0.0 > 5000) {
    currYawOri = event.orientation.x; // get current yaw orientation
    
    /* get difference between curr yaw orientation and direction of heading */
    yawDiff = currYawOri - absYawOri; 

    /* if orientation switches from 0 to 359, the difference is 359 when it should 
     actually be only 1 */ 
    if(yawDiff >= 180){
      yawDiff = 360 - yawDiff; /*calculate actual diff if auv movement is counter clockwise*/
      /* Calculate new speed of the motor when there's a yaw difference. Speed of left motor
       * increases by 1 for every change in 1 degrees. Decrease the right motor by amount 
       * of additional speed in left motor */ 
      leftSpeedPID = defaultSpeed + yawDiff;
      Serial.print("leftSpeedPID: ");
      Seial.println(leftSpeedPID);
      //rightSpeedPID = defaultSpeed - yawDiff; 
      leftEscMotor.write(leftSpeedPID); 
      //rightEscMotor.write(rightSpeedMotor);
    }else if(yawDiff < 180){ /* if motor is veering right, increase right motor speed 
      while decreasing the speed of the left motor */ 
      leftSpeedPID = defaultSpeed - yawDiff;
      Serial.print("leftSpeedPID: ");
      Serial.println(leftSpeedPID);
      //rightSpeedPID = defaultSpeed + yawDiff;
      leftEscMotor.write(leftSpeedPID);
      //rightEscMotor.write(rightSpeedPID); 
    }
     
    
  }
  

  /* Wait the specified delay before requesting nex data */
  delay(BNO055_SAMPLERATE_DELAY_MS);

}
