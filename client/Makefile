

BOARD=esp32:esp32:XIAO_ESP32C3
# BOARD=esp8266:esp8266:generic
BAUD=9600
PORT=/dev/ttyACM0
# Makefile for ESP8266-01 using arduino-cli

SRC=client.ino
BUILD=build

.PHONY: all compile flash clean

all: flash

compile:
	arduino-cli compile --fqbn $(BOARD) --output-dir $(BUILD) $(SRC)

flash: compile
	arduino-cli upload -p $(PORT) -b $(BAUD) --fqbn $(BOARD) --input-dir $(BUILD) $(SRC)

clean:
	rm -rf $(BUILD_DIR)

