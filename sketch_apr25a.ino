#include <ESP8266WiFi.h>
#include <SoftwareSerial.h>
#include <Firebase_ESP_Client.h>
#include "addons/TokenHelper.h"
#include "addons/RTDBHelper.h"         
const char* ssid = "WE_423228";
const char* password = "n3b25019";
#define FIREBASE_HOST "https://graduation-bcd1c-default-rtdb.firebaseio.com/"
#define FIREBASE_AUTH "AIzaSyBEP0Md5nWAe5vQCqGWW23XwHOMP-6BFcM"
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config; 
unsigned long sendDataPrevMillis=0;
bool signupOK = false;
///////////////////////////////////////////////////////
void setup() {
  Serial.begin(9600);
  setup_wifi();
  config.api_key = FIREBASE_AUTH;
  config.database_url = FIREBASE_HOST;
  if(Firebase.signUp(&config,&auth,"","")){Serial.print("signed up"); signupOK = true;}
  config.token_status_callback=tokenStatusCallback;
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
}
//////////////////////////////////////////////////////////
void loop() 
     {
     int value1=0;
     int value2=0;
     int value3=0;
     int value4=0;
     int value5=0;
     int value6=0;
     int value=0;
     int ecg = rand()%4 +1;
     if((digitalRead(11) == 1)||(digitalRead(10) == 1)){
     Serial.println("no reading");
      }
     else {
    value1 = analogRead(A0);
    delay(1000);
    value2 = analogRead(A0);
    delay(1000);
    value3 = analogRead(A0);
    delay(1000);
    value4 = analogRead(A0);
    delay(1000);
    value5 = analogRead(A0);
    delay(1000);
    value6 = analogRead(A0);
    delay(1000);
    value = (value1+value2+value3+value4+value5+value6)/6;
    Serial.print("ecg readings: ");
    Serial.println(value);
    delay(2000);}
    if(Firebase.ready()&&signupOK&&(millis()-sendDataPrevMillis>5000||sendDataPrevMillis==0))
    {
      sendDataPrevMillis = millis();
      if(Firebase.RTDB.setInt(&fbdo,"sensor/ECG",value)&&(Firebase.RTDB.setInt(&fbdo,"sensor/heartecg",ecg)))
      {
        Serial.println("uploaded successfully");
      }
      else{Serial.println("failed");}
    }
} 
//////////////////////////////////////////////////////////////////
void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected - ESP IP address: ");
  Serial.println(WiFi.localIP());
}
///////////////////////////////////////////////////////////////////
