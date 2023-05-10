#include <WiFi.h>
#include <WebServer.h>
const char* ssid = "cilab";
const char* password = "dogbrother";
WebServer server(80);

void handleRoot() {
  String l_elbow = server.arg("l_elbow");//2
  String r_elbow = server.arg("r_elbow");//4
  String shoulder = server.arg("shoulder");//15 16
  String hips = server.arg("hips");//22 23
  String l_knee = server.arg("l_knee");//17
  String r_knee = server.arg("r_knee");//5
  String knee = server.arg("knee");
  
  if (l_elbow=="1"){
    Serial.println("l_elbow="+l_elbow);
    server.send(200, "text/plain", "l_elbow");
    digitalWrite(2,HIGH);
    delay(1000);
    digitalWrite(2,LOW);
  }else if(r_elbow=="1"){
    Serial.println("r_elbow="+r_elbow);
    server.send(200, "text/plain", "r_elbow");
    digitalWrite(4,HIGH);
    delay(1000);
    digitalWrite(4,LOW);
  }else if(shoulder=="1"){
    Serial.println("shoulder="+shoulder);
    server.send(200, "text/plain", "shoulder");
    digitalWrite(15,HIGH);
    digitalWrite(16,HIGH);
    delay(1000);
    digitalWrite(15,LOW);
    digitalWrite(16,LOW);
  }else if(hips=="1"){
    Serial.println("hip="+hips);
    server.send(200, "text/plain", "hips");
    digitalWrite(22,HIGH);
    digitalWrite(23,HIGH);
    delay(1000);
    digitalWrite(22,LOW);
    digitalWrite(23,LOW);
  }else if(l_knee=="1"){
    Serial.println("l_knee="+l_knee);
    server.send(200, "text/plain", "l_knee");
    digitalWrite(17,HIGH);
    delay(1000);
    digitalWrite(17,LOW);
  }else if(r_knee=="1"){
    Serial.println("r_knee="+r_knee);
    server.send(200, "text/plain", "r_knee");
    digitalWrite(5,HIGH);
    delay(1000);
    digitalWrite(5,LOW);
  }else if(knee=="1"){
    Serial.println("knee="+knee);
    server.send(200, "text/plain", "knee");
    digitalWrite(5,HIGH);
    digitalWrite(17,HIGH);
    delay(1000);
    digitalWrite(5,LOW);
    digitalWrite(17,LOW);
  }

}
//15,2,4,16,17,5
void setup() {
pinMode(15,OUTPUT);
pinMode(2,OUTPUT);
pinMode(4,OUTPUT);
pinMode(16,OUTPUT);
pinMode(13,OUTPUT);
pinMode(22,OUTPUT);
pinMode(23,OUTPUT);
pinMode(17,OUTPUT);
pinMode(5,OUTPUT);
  
Serial.begin(115200);
WiFi.begin(ssid, password);
while (WiFi.status() != WL_CONNECTED) {
  Serial.println(".");
  delay(1000);
  digitalWrite(13,LOW);

}
Serial.println("WiFi connected");
Serial.println(WiFi.localIP());
digitalWrite(13,HIGH);
server.on("/",handleRoot);
server.begin();             
}

void loop() {
server.handleClient();
}
