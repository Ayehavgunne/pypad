#pragma once
#include <ArduinoJson.h>

StaticJsonDocument<5120> key_codes;

void set_key_codes() {
  key_codes["LCTRL"] = KEY_LEFT_CTRL;
  key_codes["CTRL"] = MODIFIERKEY_CTRL;
  key_codes["RCTRL"] = KEY_RIGHT_CTRL;
  key_codes["LSHIFT"] = KEY_LEFT_SHIFT;
  key_codes["SHIFT"] = MODIFIERKEY_SHIFT;
  key_codes["RSHIFT"] = KEY_RIGHT_SHIFT;
  key_codes["LALT"] = KEY_LEFT_ALT;
  key_codes["ALT"] = MODIFIERKEY_ALT;
  key_codes["RALT"] = KEY_RIGHT_ALT;
  key_codes["LMETA"] = KEY_LEFT_GUI;
  key_codes["LGUI"] = KEY_LEFT_GUI;
  key_codes["META"] = MODIFIERKEY_GUI;
  key_codes["GUI"] = MODIFIERKEY_GUI;
  key_codes["RMETA"] = KEY_RIGHT_GUI;
  key_codes["RGUI"] = KEY_RIGHT_GUI;
  key_codes["A"] = KEY_A;
  key_codes["B"] = KEY_B;
  key_codes["C"] = KEY_C;
  key_codes["D"] = KEY_D;
  key_codes["E"] = KEY_E;
  key_codes["F"] = KEY_F;
  key_codes["G"] = KEY_G;
  key_codes["H"] = KEY_H;
  key_codes["I"] = KEY_I;
  key_codes["J"] = KEY_J;
  key_codes["K"] = KEY_K;
  key_codes["L"] = KEY_L;
  key_codes["M"] = KEY_M;
  key_codes["N"] = KEY_N;
  key_codes["O"] = KEY_O;
  key_codes["P"] = KEY_P;
  key_codes["Q"] = KEY_Q;
  key_codes["R"] = KEY_R;
  key_codes["S"] = KEY_S;
  key_codes["T"] = KEY_T;
  key_codes["U"] = KEY_U;
  key_codes["V"] = KEY_V;
  key_codes["W"] = KEY_W;
  key_codes["X"] = KEY_X;
  key_codes["Y"] = KEY_Y;
  key_codes["Z"] = KEY_Z;
  key_codes["CAPS_LOCK"] = KEY_CAPS_LOCK;
  key_codes["ENTER"] = KEY_RETURN;
  key_codes["RETURN"] = KEY_RETURN;
  key_codes["BACKSPACE"] = KEY_BACKSPACE;
  key_codes["SPACE"] = KEY_SPACE;
  key_codes["TAB"] = KEY_TAB;
  key_codes["ESC"] = KEY_ESC;
  key_codes["ESCAPE"] = KEY_ESC;
  key_codes["INSERT"] = KEY_INSERT;
  key_codes["DELETE"] = KEY_DELETE;
  key_codes["HOME"] = KEY_HOME;
  key_codes["END"] = KEY_END;
  key_codes["PAGE_UP"] = KEY_PAGE_UP;
  key_codes["PAGE_DOWN"] = KEY_PAGE_DOWN;
  key_codes["RIGHT"] = KEY_RIGHT_ARROW;
  key_codes["LEFT"] = KEY_LEFT_ARROW;
  key_codes["UP"] = KEY_UP_ARROW;
  key_codes["DOWN"] = KEY_DOWN_ARROW;
  key_codes["SCROLL_LOCK"] = KEY_SCROLL_LOCK;
  key_codes["PAUSE"] = KEY_PAUSE;
  key_codes["1"] = KEY_1;
  key_codes["2"] = KEY_2;
  key_codes["3"] = KEY_3;
  key_codes["4"] = KEY_4;
  key_codes["5"] = KEY_5;
  key_codes["6"] = KEY_6;
  key_codes["7"] = KEY_7;
  key_codes["8"] = KEY_8;
  key_codes["9"] = KEY_9;
  key_codes["0"] = KEY_0;
  key_codes["MINUS"] = KEY_MINUS;
  key_codes["EQUAL"] = KEY_EQUAL;
  key_codes["LEFT_BRACE"] = KEY_LEFT_BRACE;
  key_codes["RIGHT_BRACE"] = KEY_RIGHT_BRACE;
  key_codes["BACKSLASH"] = KEY_BACKSLASH;
  key_codes["SEMICOLON"] = KEY_SEMICOLON;
  key_codes["APOSTROPHE"] = KEY_SEMICOLON;
  key_codes["GRAVE"] = KEY_TILDE;
  key_codes["BACKTICK"] = KEY_TILDE;
  key_codes["COMMA"] = KEY_COMMA;
  key_codes["DOT"] = KEY_PERIOD;
  key_codes["PERIOD"] = KEY_PERIOD;
  key_codes["SLASH"] = KEY_SLASH;
  key_codes["F1"] = KEY_F1;
  key_codes["F2"] = KEY_F2;
  key_codes["F3"] = KEY_F3;
  key_codes["F4"] = KEY_F4;
  key_codes["F5"] = KEY_F5;
  key_codes["F6"] = KEY_F6;
  key_codes["F7"] = KEY_F7;
  key_codes["F8"] = KEY_F8;
  key_codes["F9"] = KEY_F9;
  key_codes["F10"] = KEY_F10;
  key_codes["F11"] = KEY_F11;
  key_codes["F12"] = KEY_F12;
  key_codes["PRINT_SCREEN"] = KEY_PRINTSCREEN;
  key_codes["NUMLOCK"] = KEY_NUM_LOCK;
  key_codes["KEYPAD_SLASH"] = KEYPAD_SLASH;
  key_codes["KEYPAD_ASTERISK"] = KEYPAD_ASTERIX;
  key_codes["KEYPAD_MINUS"] = KEYPAD_MINUS;
  key_codes["KEYPAD_PLUS"] = KEYPAD_PLUS;
  key_codes["KEYPAD_ENTER"] = KEYPAD_ENTER;
  key_codes["KEYPAD_1"] = KEYPAD_1;
  key_codes["KEYPAD_2"] = KEYPAD_2;
  key_codes["KEYPAD_3"] = KEYPAD_3;
  key_codes["KEYPAD_4"] = KEYPAD_4;
  key_codes["KEYPAD_5"] = KEYPAD_5;
  key_codes["KEYPAD_6"] = KEYPAD_6;
  key_codes["KEYPAD_7"] = KEYPAD_7;
  key_codes["KEYPAD_8"] = KEYPAD_8;
  key_codes["KEYPAD_9"] = KEYPAD_9;
  key_codes["KEYPAD_0"] = KEYPAD_0;
  key_codes["KEYPAD_DOT"] = KEYPAD_PERIOD;
  key_codes["KEYPAD_PERIOD"] = KEYPAD_PERIOD;
}
