#include <WiFi.h>
#include <AsyncUDP.h>
#include <LiquidCrystal_I2C.h>

// File should have the following
// const char* ssid = "<YOUR SSID>";
// const char* password = "<YOUR WIFI PASSOWRD>";
#include "WiFiCredentials.h"

#include "characters.h"


IPAddress staticLocalIp(192, 168, 1, 180);
IPAddress gateway(192,168,1,1);
IPAddress subnetMask(255,255,255, 0);
IPAddress dns1(8,8,8,8);
IPAddress dns2(8,8,8,8);

const char* hostname = "esp32MoneyTrkr";

char packetBuffer[255]; //buffer to hold incoming packet
char  ReplyBuffer[] = "Rodger";       // a string to send back

// Set the LCD address to 0x27 for a 16 chars and 2 line display
LiquidCrystal_I2C lcd(0x27, 16, 2);

AsyncUDP udp;

void onUdpPacket(AsyncUDPPacket pkt){
    lcd.setCursor(0,0);
    String msg = pkt.readString();

    // Ensure message is at least 32 characters
    while (msg.length() < 32) {
        msg += " "; // pad with spaces if too short
    }

    // Display first 16 chars on row 0
    lcd.setCursor(0, 0);
    lcd.print(msg.substring(0, 16));

    // Display next 16 chars on row 1
    lcd.setCursor(0, 1);
    lcd.print(msg.substring(16, 32));
}

void setup() {
    lcd.init();                      // Initialize the LCD


    // Initalize custom characters from characters.h
    lcd.createChar(1, one);
    lcd.createChar(2, two);
    lcd.createChar(3, three);
    lcd.createChar(4, four);
    lcd.createChar(5, full);

    lcd.backlight();                 // Turn on the backlight

    lcd.setCursor(0, 0);
    lcd.print("Conn to network");

    WiFi.setHostname(hostname);
    WiFi.config(staticLocalIp, gateway, subnetMask, dns1, dns2);
    WiFi.begin(ssid, password);

    int retries = 0;
    while (WiFi.status() != WL_CONNECTED && retries < 20) {
        delay(500);
        lcd.setCursor(retries % 16, 1);
        lcd.print(".");
        retries++;
    }

    lcd.clear();
    if (WiFi.status() == WL_CONNECTED) {
        lcd.setCursor(0, 0);
        lcd.print("WiFi Connected!");
        lcd.setCursor(0, 1);
        lcd.print(WiFi.localIP());
        delay(3000);
    } else {
      lcd.setCursor(0, 0);
      lcd.print("WiFi Failed");
      lcd.setCursor(0, 1);
      lcd.print("Reboot Device");
      while(1){}
    }

    if (udp.listen(9877)) {
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("lstn on prt 9877");
      lcd.setCursor(0,1);
      lcd.print("Send away!");
      udp.onPacket(onUdpPacket);
    }
}


void loop() {}

