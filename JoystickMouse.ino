// Arduino Nano Joystick Reader
// Reads analog joystick X/Y positions and sends them over Serial for mouse
// control.

const int VRX = A0; // Joystick X-axis pin
const int VRY = A1; // Joystick Y-axis pin

void setup() {
  // Initialize high-speed serial communication
  Serial.begin(250000);
}

void loop() {
  // Read joystick axis values (0–1023)
  int x = analogRead(VRX);
  int y = analogRead(VRY);

  // Send data in "x,y" format
  Serial.print(x);
  Serial.print(",");
  Serial.println(y);

  // Small delay for stable and responsive updates
  delay(5);
}