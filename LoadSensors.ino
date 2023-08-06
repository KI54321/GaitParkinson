#include <HX711.h>
#include <HTTPClient.h>
#include <WiFi.h>


#define DOUT  P6_1
#define CLK  P4_0

char* wifiSSID = "eec172";

HX711 scale;

void setup() {
  Serial.begin(115200);
  Serial.write("Hello");
  setUpWifiConnection();
  scale.begin(DOUT, CLK);
  scale.set_scale(8507); // This value is obtained by calibrating the scale with known weights
  scale.tare(); // Tare the scale using a known weight
  Serial.write("HOla");
}

void loop() {
  
  long weightReading = scale.get_units(10); // Read the weight (average over 10 readings)

  Serial.print("Weight: ");
  Serial.print(weightReading);
  Serial.println(" grams");

  delay(1000); // 1-second delay
}


void setUpWifiConnection() {
  WiFi.begin(wifiSSID);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting...");
  }
  Serial.println("Done. Connected!");


}

void makeGaitRequest() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient gaitHTTP;
    String gaitServer = "google.com";
    gaitHTTP.begin(gaitServer.c_str());
    gaitHTTP.GET();
    Serial.println("Gait API Called")
    gaitHTTP.end()
  }
}
