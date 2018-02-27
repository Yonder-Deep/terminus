int analogPin = 3; 
int val = 0; 
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); 
  Serial.println("starting!!");

}

void loop() {
  
  // put your main code here, to run repeatedly:
  val = analogRead(analogPin);
  Serial.print("Hydrophone of: ");
  Serial.println(val);
    
}
