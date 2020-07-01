# pypad
###### python/arduino based keypad with analog joystick for games/macros

### Goals
What I wanted was to replace my Razer Tartarus V2 with it's crappy d-pad and bloated software. There is a long-standing
bug where sometimes the d-pad input gets stuck and you have to hit it again in the same direction and let go to get it
to stop. I'm done waiting for them to fix it! I want a real analog joystick! I want mechanical switches! I want the
profiles to automatically switch when I launch a new game, something I think Synapse is supposed to do but it doesn't
work for me! I want to uninstall Synapse! I don't want to give up anything that the Tartarus does right! I want a
million dollars!

I have been able to achieve almost all of these goals. Who knows, maybe I can still get the last one.

### How it works
I designed a series of custom PCBs and had them made by [JLCPCB](https://jlcpcb.com/). They fit snugly into the shell of
a Razer Tartarus V2. The PCBs connect the 1-19 switches of the main section, the scroll wheel and scroll button, an
analog joystick and the joystick pushbutton, and finally, buttons 20 and 21 for the thumb, all to a Teensy 3.6.

The Teensy acts as a USB HID Keyboard/Mouse/Joystick all at the same time. I send it maps of keyboard keys, mouse
buttons, gamepad buttons or joystick directions (actions) to its keyboard switches, scroll wheel directions, various
other buttons (inputs). Triggering an input executes the corresponding action.

I was able to add an NKRO USB device to the Teensyduino code with this 
[patch](https://gist.github.com/onebytegone/70de13831afa516dafb7e210da0f6368). Getting the analog joystick to work with
modern games was not fun. Eventually, though, I found a program called
[World of Joysticks](https://www.worldofjoysticks.com/) that simply translates the DirectInput protocol used by the
Teensyduino to the newer XInput protocol. I had zero luck with x360ce. Now that I have actual controller capabilites I
will add joystick buttons as possible actions to be tiggered by the inputs.

I did build in a WASD_MODE where the joystick gets mapped to WASD (or any other keys) and triggers the keydown if it
goes beyond specific thresholds. This works for games that either don't support controllers or that don't work with
simultanious keyboard/mouse and controller input.

A python program runs in the background on the computer and connects to the Teensy through a serial connection. It then
monitors for processes that are listed in the mappings.yaml file. When a process is detected the associated key mappings
will be sent over serial in UTF-8 JSON format to the Teensy. Edits to the mappings.yaml file will be sent to the Teensy
after only a short delay. I have started working on a web interface that will make changing out the mappings and various
options easier. I will probably turn the python monitoring program into a Windows service so that it can always be
running.

### Features
- 20 low profile Kailh Choc Navy switches, 1 scroll wheel with middle button, 1 simple button, 1 analog joystick with
pushbutton
- ability to map any keyboard key, mouse button, mouse scroll action, joystick direction, joystick buttons to any input
on the keypad 
- ability to rotate the XY axis of the joystick by any angle to accommodate the placement of the thumb and installation
angle of the joystick module
- ability to change mappings on the fly
- web interface to make changing the mappings and other options quick and easy
- automatic swapping of map profiles when new programs are launched
- ability to reprogram the Teensy without disassembly 

### Status
This is mostly complete and I can use it right now to play games! I must say it works rather well. There are still some
minor issues to be worked out in the software on both the Teensy and Python side of things but those won't take too long
to address.

<img src="https://raw.githubusercontent.com/Ayehavgunne/pypad/master/hardware1.jpg" width="500" title="results">
<br>
<br>
<img src="https://raw.githubusercontent.com/Ayehavgunne/pypad/master/hardware2.jpg" width="500" title="pcbs">

### TODO
In Python
- finish web interface
- fix bug with monitor not connecting after unplugging and replugging Teensy

On Teensy
- keep track of mouse button down and mouse button up events to prevent spamming those actions
- add joystick/gamepad/controller (whatever you want to call it) buttons as possible actions
- add deadzone configs to analog joystick
- add more debug output maybe?
