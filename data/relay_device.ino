#include <avr/sleep.h>
#include <avr/wdt.h>

const int ledPin = 13;       // Built-in LED pin to indicate wake state
const unsigned long sleepTimeMs = 3000;  // Sleep time in milliseconds

volatile bool watchdogInterruptTriggered = false;

void setup() {
  pinMode(ledPin, OUTPUT);    // Set LED pin as output
  wdt_disable();              // Disable Watchdog Timer at startup
}

void loop() {
  // Wake up for 5 seconds
  digitalWrite(ledPin, HIGH); // Turn on LED to indicate wake state
  delay(3000);                // Keep the Arduino awake for 5 seconds

  // Sleep for a specified duration
  digitalWrite(ledPin, LOW);  // Turn off LED to indicate sleep state
  goToSleep(sleepTimeMs);     // Pass sleep time in milliseconds
}

void goToSleep(unsigned long sleepDuration) {
  unsigned long sleptTime = 0;

  while (sleptTime < sleepDuration) {
    // Set Watchdog Timer for a 1-second interval
    wdt_enable(WDTO_1S);
    WDTCSR |= (1 << WDIE);    // Enable Watchdog Interrupt mode

    // Set sleep mode to Power-down for low power consumption
    set_sleep_mode(SLEEP_MODE_PWR_DOWN);
    sleep_enable();           // Enable sleep mode

    // Enter sleep mode and wait for Watchdog Timer interrupt
    watchdogInterruptTriggered = false;
    sleep_cpu();

    // After waking up
    sleep_disable();
    wdt_disable();            // Disable the watchdog to avoid auto-resets

    // Check if watchdog interrupt triggered wakeup
    if (watchdogInterruptTriggered) {
      sleptTime += 1000;      // Increment slept time by 1 second (1000 ms)
    }
  }
}

// Watchdog Timer Interrupt Service Routine
ISR(WDT_vect) {
  watchdogInterruptTriggered = true; // Set flag to indicate WDT wake-up
}
