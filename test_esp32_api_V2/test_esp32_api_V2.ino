#include <WiFi.h>

// Replace with your network credentials
const char* ssid = "Jiye";
const char* password = "123456987";

WiFiServer server(80); // Create a server object that listens on port 80

void setup() {
  Serial.begin(9600);
  delay(1000);

  // Connect to Wi-Fi network with SSID and password
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("WiFi connected.");
  Serial.print("Server started at ");
  Serial.println(WiFi.localIP()); // Print the IP address of ESP32

  server.begin(); // Start the server
}

void loop() {
  WiFiClient client = server.available(); // Check if a client has connected

  if (client) {
    Serial.println("New client connected.");

    while (client.connected()) {
      if (client.available()) {
        String data = client.readStringUntil('\n'); // Read the data from client

        Serial.print("Data received: ");
        Serial.println(data); // Print the received data

        client.print("Data received: "); // Send a response to client
        client.println(data);
      }
    }

    Serial.println("Client disconnected."); // When the client is disconnected
  }
}
