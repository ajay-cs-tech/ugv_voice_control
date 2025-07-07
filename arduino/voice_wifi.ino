#include <WiFiS3.h>

// AP credentials
char ssid[] = "UGV-NETWORK";
char pass[] = "ugv123456";

WiFiServer server(80);

void setup() {
  Serial.begin(9600);

  // Set motor pins
  pinMode(9, OUTPUT);    // ENA
  pinMode(10, OUTPUT);   // ENB
  pinMode(2, OUTPUT);    // IN1
  pinMode(4, OUTPUT);    // IN2
  pinMode(7, OUTPUT);    // IN3
  pinMode(8, OUTPUT);    // IN4
  stopMotors();

  // Start AP
  Serial.println("Starting Access Point...");
  WiFi.beginAP(ssid, pass);

  IPAddress IP = WiFi.localIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);

  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    String request = client.readStringUntil('\r');
    client.flush();

    if (request.indexOf("/forward") != -1) moveForward();
    else if (request.indexOf("/backward") != -1) moveBackward();
    else if (request.indexOf("/left") != -1) turnLeft();
    else if (request.indexOf("/right") != -1) turnRight();
    else if (request.indexOf("/stop") != -1) stopMotors();

    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/plain");
    client.println("Connection: close");
    client.println();
    client.println("OK");
  }
}

// Movement functions...

void moveForward() {
  digitalWrite(2, HIGH); digitalWrite(4, LOW);
  digitalWrite(7, HIGH); digitalWrite(8, LOW);
  analogWrite(9, 200); analogWrite(10, 200);
}

void moveBackward() {
  digitalWrite(2, LOW); digitalWrite(4, HIGH);
  digitalWrite(7, LOW); digitalWrite(8, HIGH);
  analogWrite(9, 200); analogWrite(10, 200);
}

void turnLeft() {
  digitalWrite(2, LOW); digitalWrite(4, HIGH);
  digitalWrite(7, HIGH); digitalWrite(8, LOW);
  analogWrite(9, 200); analogWrite(10, 200);
}

void turnRight() {
  digitalWrite(2, HIGH); digitalWrite(4, LOW);
  digitalWrite(7, LOW); digitalWrite(8, HIGH);
  analogWrite(9, 200); analogWrite(10, 200);
}

void stopMotors() {
  digitalWrite(2, LOW); digitalWrite(4, LOW);
  digitalWrite(7, LOW); digitalWrite(8, LOW);
  analogWrite(9, 0); analogWrite(10, 0);
}
