// Ultrasonic sensor
int frontEchoPin = A0;
int frontTrigPin = A1;

int leftEchoPin = A2;
int leftTrigPin = A3;

int rightEchoPin = A4;
int rightTrigPin = A5;



// Anything over 400 cm (23200 us pulse) is "out of range"
const unsigned int MAX_ECHO_US = 23200;
const unsigned int MAX_DIST_MM = 4000;

const int SONAR_DELAY_US = 10;
int front_us1 = MAX_DIST_MM;
int left_us1 = MAX_DIST_MM;
int right_us1 = MAX_DIST_MM;

void setup() {
  Serial.begin(9600);
  // Set pin directions for the ultrasonic sensor
  pinMode(frontEchoPin, INPUT);
  pinMode(frontTrigPin, OUTPUT);
  
  pinMode(leftEchoPin, INPUT);
  pinMode(leftTrigPin, OUTPUT);
  
  pinMode(rightEchoPin, INPUT);
  pinMode(rightTrigPin, OUTPUT);

}

void loop()
{
  // Get distance from wall with ultrasonic sensor
  front_us1 = getFronttUS1();
  left_us1 = getLeftUS1();
  right_us1 = getRightUS1();

  // Read everything from serial
  if(Serial.available())   
  {
    Serial.read(); 
    
    // Print data to serial.
    printJSON(front_us1, left_us1, right_us1);
  } 
}

// Gets distance in mm from the ultrasonic sensor
long getFronttUS1(){
  digitalWrite(frontTrigPin, HIGH);
  delayMicroseconds(SONAR_DELAY_US);
  digitalWrite(frontTrigPin, LOW);
  long duration = pulseIn(frontEchoPin, HIGH, MAX_ECHO_US);
  return (duration/2) / 2.91; // get distance in mm
}

long getLeftUS1(){
  digitalWrite(leftTrigPin, HIGH);
  delayMicroseconds(SONAR_DELAY_US);
  digitalWrite(leftTrigPin, LOW);
  long duration = pulseIn(leftEchoPin, HIGH, MAX_ECHO_US);
  return (duration/2) / 2.91; // get distance in mm
}

long getRightUS1(){
  digitalWrite(rightTrigPin, HIGH);
  delayMicroseconds(SONAR_DELAY_US);
  digitalWrite(rightTrigPin, LOW);
  long duration = pulseIn(rightEchoPin, HIGH, MAX_ECHO_US);
  return (duration/2) / 2.91; // get distance in mm
}

// Print all the sensor data to serial as JSON
void printJSON(int front_us1, int left_us1, int right_us1) 
{ 
  Serial.print("{\"front_us1\":");
  Serial.print(front_us1);
  Serial.print(", \"left_us1\":");
  Serial.print(left_us1);
  Serial.print(", \"right_us1\":");
  Serial.print(right_us1);
  Serial.println("}");
}
