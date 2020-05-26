# pypad
python based keypad with joystick for games/macros

It's called PyPad because that was the least crappy name I could think of right
now.

Using a pyboard, I have wired up a bunch of keyboard switches to the multitude of
pins and I am using that to detect a keypress. I then send that information over
a USB connection to the main program running on my computer. This reads the keys
that are currently being pressed and then sends the keystrokes via SendInput
which most games seem to accept. I am having issues with PSO2 though which I
figure is because of GameGuard (I'm not cheating! I swear!). The program that
runs on the computer scans for processes by the exe name and will load up
different profiles for multiple games.

I am in the middle of adding a joystick to the mix for easy character movement.
Due to the different requirements of various games I plan in having the ability
to switch between actual joystick gamepad (for real analog input) and mapping
it to wasd.

The goal is to replace my Razer Tartarus V2 with it's crappy digital 8
directional joystick and bloated software. There is a reported problem that is
still not fixed where sometimes the joystick input gets stuck and you have to
hit it again in the same direction and let go to get it to stop. Really
anoying :(
