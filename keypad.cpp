#include <ArduinoJson.h>

#include "Arduino.h"
#include "key_codes.h"
#include "mouse_codes.h"

#define ON HIGH
#define NUM_OF_PINS 21
#define JOY_BUTTON 18
#define JOY_X 5
#define JOY_Y 6
#define ROTARY_1 21
#define ROTARY_2 22
#define SCROLL_MIDDLE 0
#define SERIAL_READ_TIMEOUT 500.0
#define RAD_TO_DEG 57.295779513082320876798154814105

const unsigned int PINS[NUM_OF_PINS] = {
	30, 26, 11, 7, 3, 29, 25, 10, 6, 2, 28, 24, 9, 5, 1, 27, 12, 8, 4, 16, 17};
DynamicJsonDocument key_map(5120);
unsigned int joy_x_deadzone = 200;
unsigned int joy_y_deadzone = 200;
unsigned int joy_x_center = 530;
unsigned int joy_y_center = 502;
unsigned int joy_x_y_rotation = 15;
bool wasd_mode = true;
bool debug_mode = false;
int rotary_1_last;
int rotary_1_state;

void setup() {
	set_key_codes();
	set_mouse_codes();

	for (int i = 0; i < NUM_OF_PINS; i++) {
		pinMode(PINS[i], INPUT_PULLDOWN);
	}

	pinMode(JOY_BUTTON, INPUT_PULLUP);
	pinMode(ROTARY_1, INPUT_PULLDOWN);
	pinMode(ROTARY_2, INPUT_PULLDOWN);
	pinMode(SCROLL_MIDDLE, INPUT_PULLDOWN);

	rotary_1_last = digitalRead(ROTARY_1);
}

void get_key_map() {
	if (Serial.available() > 0) {
		String json_data = Serial.readString();
		unsigned long start = millis();
		while (json_data.indexOf('\n') == -1) {
			json_data.concat(Serial.readString());
			if (millis() - start > SERIAL_READ_TIMEOUT) {
				break;
			}
		}
		DeserializationError err = deserializeJson(key_map, json_data);
		if (err != DeserializationError::Ok) {
			if (debug_mode) {
				Serial.print("Deserialize failed\t");
			}
			key_map.clear();
		}
		else {
			if (key_map.containsKey("WASD_MODE")) {
				wasd_mode = key_map["WASD_MODE"] == "TRUE";
			}
			if (key_map.containsKey("DEBUG")) {
				debug_mode = key_map["DEBUG"] == "TRUE";
			}
			if (key_map.containsKey("JOY_X_CENTER")) {
				joy_x_center = strtol(key_map["JOY_X_CENTER"], NULL, 10);
			}
			if (key_map.containsKey("JOY_Y_CENTER")) {
				joy_y_center = strtol(key_map["JOY_Y_CENTER"], NULL, 10);
			}
			if (key_map.containsKey("JOY_X_DEADZONE")) {
				joy_x_deadzone = strtol(key_map["JOY_X_DEADZONE"], NULL, 10);
			}
			if (key_map.containsKey("JOY_Y_DEADZONE")) {
				joy_y_deadzone = strtol(key_map["JOY_Y_DEADZONE"], NULL, 10);
			}
			if (key_map.containsKey("JOY_X_Y_ROTATION")) {
				joy_x_y_rotation = strtol(key_map["JOY_X_Y_ROTATION"], NULL, 10);
			}
			if (key_map.containsKey("PROG") && key_map["PROG"] == "TRUE") {
				_reboot_Teensyduino_();
			}
			if (debug_mode) {
				Serial.print("Deserialize success\t");
			}
		}
	}
}

void check_keys() {
	for (int i = 0; i < NUM_OF_PINS; i++) {
		if (digitalRead(PINS[i]) == ON) {
			String key_num = String(i + 1);
			if (key_map.containsKey(key_num)) {
				check_for_actions(key_num);
			}
		}
	}
}

void check_other_buttons() {
	if (key_map.containsKey("JOY_BUTTON")) {
		if (digitalRead(JOY_BUTTON) == LOW) {
			check_for_actions("JOY_BUTTON");
		}
	}
	if (key_map.containsKey("SCROLL_MIDDLE")) {
		if (digitalRead(SCROLL_MIDDLE) == ON) {
			check_for_actions("SCROLL_MIDDLE");
		}
	}
}

void check_joystick() {
	float joy_x = analogRead(JOY_X) - (float)joy_x_center;
	float joy_y = analogRead(JOY_Y) - (float)joy_y_center;
	if (joy_x_y_rotation != 0) {
		float cos_angle = cos(joy_x_y_rotation / RAD_TO_DEG);
		float sin_angle = sin(joy_x_y_rotation / RAD_TO_DEG);
		float joy_x_old = joy_x;
		float joy_y_old = joy_y;
		joy_x = joy_x_old * cos_angle + joy_y_old * sin_angle;
		joy_y = -joy_x_old * sin_angle + joy_y_old * cos_angle;
	}
	joy_x = joy_x + joy_x_center;
	joy_y = joy_y + joy_y_center;
	if (wasd_mode) {
		if (key_map.containsKey("JOY_UP")) {
			if (joy_y > joy_y_center + joy_y_deadzone) {
				check_for_actions("JOY_UP");
			}
		}
		if (key_map.containsKey("JOY_DOWN")) {
			if (joy_y < joy_y_center - joy_y_deadzone) {
				check_for_actions("JOY_DOWN");
			}
		}
		if (key_map.containsKey("JOY_LEFT")) {
			if (joy_x < joy_x_center - joy_x_deadzone) {
				check_for_actions("JOY_LEFT");
			}
		}
		if (key_map.containsKey("JOY_RIGHT")) {
			if (joy_x > joy_x_center + joy_x_deadzone) {
				check_for_actions("JOY_RIGHT");
			}
		}
	}
	else {
		Joystick.X(joy_x);
		Joystick.Y(joy_y);
	}
	if (debug_mode) {
		Serial.print("X: ");
		Serial.print(joy_x);
		Serial.print("\tY: ");
		Serial.print(joy_y);
		Serial.print("\r\n");
	}
}

void rotary_detection() {
	if (key_map.containsKey("SCROLL_UP") || key_map.containsKey("SCROLL_DOWN")) {
		rotary_1_state = digitalRead(ROTARY_1);
		if (rotary_1_state != rotary_1_last) {
			if (digitalRead(ROTARY_2) != rotary_1_state) {
				check_for_actions("SCROLL_DOWN");
			}
			else {
				check_for_actions("SCROLL_UP");
			}
		}
		rotary_1_last = rotary_1_state;
	}
}

void check_for_actions(String map_key) {
	String code_key = key_map[map_key];
	if (check_scroll_action(code_key)) {
		return;
	}
	if (check_key_action(code_key)) {
		return;
	}
	if (check_mouse_action(code_key)) {
		return;
	}
}

bool check_scroll_action(String code_key) {
	if (code_key == "SCROLL_UP") {
		Mouse.move(0, 0, 1);
		return true;
	}
	else if (code_key == "SCROLL_DOWN") {
		Mouse.move(0, 0, -1);
		return true;
	}
	return false;
}

bool check_key_action(String code_key) {
	if (key_codes.containsKey(code_key)) {
		unsigned int code = key_codes[code_key];
		Nkro.set_key(code);
		return true;
	}
	return false;
}

bool check_mouse_action(String code_key) {
	if (mouse_codes.containsKey(code_key)) {
		unsigned int code = mouse_codes[code_key];
		Mouse.press(code);
		return true;
	}
	return false;
}

void loop() {
	get_key_map();
	Nkro.reset_keys();
	rotary_detection();

	if (!key_map.isNull()) {
		check_keys();
		check_other_buttons();
		check_joystick();
	}

	Nkro.send_nkro_now();
	delay(5);
}
