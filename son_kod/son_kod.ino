#include <SPI.h>
#include <MFRC522.h>
#include <LiquidCrystal.h>

LiquidCrystal lcd(7, 6, 5, 4, 3, 2);
int buzzerPin = 8; // Define the buzzer pin

#define RST_PIN 9
#define SS_PIN 10

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance.

void setup() {
    Serial.begin(9600);
    lcd.begin(16, 2);
    lcd.print("Scan card");
    pinMode(buzzerPin, OUTPUT); // Set the buzzer pin as an output
    while (!Serial);
    SPI.begin();			// Init SPI bus
	  mfrc522.PCD_Init();		// Init MFRC522
	  delay(4);				// Optional delay. Some board do need more time after init to be ready, see Readme
	  mfrc522.PCD_DumpVersionToSerial();	// Show details of PCD - MFRC522 Card Reader details
	  Serial.println(F("Scan PICC to see UID, SAK, type, and data blocks..."));
}
bool uidRead = false; // Flag to track if UID has been read

void loop() {
  // ... (rest of the code remains the same)

  if (mfrc522.PICC_IsNewCardPresent()) {
    if (mfrc522.PICC_ReadCardSerial() && !uidRead) {
      // Print only the UID (only if not already read)
      lcd.clear();
      lcd.print("Card scanned");
      beep(); // Make the buzzer beep when card is scanned
      for (byte i = 0; i < mfrc522.uid.size; i++) {
        Serial.print(mfrc522.uid.uidByte[i], HEX);
        if (i < mfrc522.uid.size - 1) {
          Serial.print(" ");
        }
      }
      Serial.println();
      uidRead = true;  // Mark UID as read
      delay(5000); // Wait for 5 seconds
      lcd.clear();
      lcd.print("Scan card"); // Display default message
    }
  } else {
    // Reset the flag if no card is present
    uidRead = false;
  }
}


void beep() {
    // Make the buzzer beep for 5 seconds
    for (int i = 0; i < 5; i++) {
        digitalWrite(buzzerPin, HIGH);
        delay(100);
        digitalWrite(buzzerPin, LOW);
        delay(100);
    }
}