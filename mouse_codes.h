#pragma once
#include <ArduinoJson.h>

StaticJsonDocument<5120> mouse_codes;

void set_mouse_codes() {
  mouse_codes["MOUSE_1"] = MOUSE_LEFT;
  mouse_codes["MOUSE_LEFT"] = MOUSE_LEFT;
  mouse_codes["MOUSE_2"] = MOUSE_RIGHT;
  mouse_codes["MOUSE_RIGHT"] = MOUSE_RIGHT;
  mouse_codes["MOUSE_3"] = MOUSE_MIDDLE;
  mouse_codes["MOUSE_MIDDLE"] = MOUSE_MIDDLE;
  mouse_codes["SCROLL_MIDDLE"] = MOUSE_MIDDLE;
  mouse_codes["MOUSE_4"] = MOUSE_BACK;
  mouse_codes["MOUSE_BACK"] = MOUSE_BACK;
  mouse_codes["MOUSE_5"] = MOUSE_FORWARD;
  mouse_codes["MOUSE_FORWARD"] = MOUSE_FORWARD;
}
