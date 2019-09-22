# ding-pi
Turn your raspberry pi 3 into a midi usb host/router/midi processor by way of mididings!

![photo of raspberry pi 3 with usb devices plugged in](https://github.com/esaumusic/ding-pi/blob/master/images/IMG-3204.JPG)

ESAU's DingPi Script (no this isn't chinese food, this turns your raspberry pi 3 into a midi usb host/router/midi processor by way of MidiDings!)

## Prerequisites
+ Raspberry Pi 3/3+ (other models untested but might work)
+ Installed Raspbian Stretch Lite (https://www.raspberrypi.org/downloads/raspbian/)
+ Installed alsa utilities (sudo apt-get install alsa-utils if connected to internet)
+ Installed mididings (sudo apt-get install mididings if connected to internet) mididings documentation: http://dsacre.github.io/mididings/doc/start.html

## Recommended
+ Wifi enabled for quick installation of prerequisites
+ If you don't use linux much like me, enabling ssh on your pi so you can remote from another computer on your home network is pretty slick.
+ Use linux utility crontab or equivalent to run this script on startup so you don't need a keyboard/monitorself. tutorial here: https://www.dexterindustries.com/howto/auto-run-python-programs-on-the-raspberry-pi/

## Overview of MIDI hardware involved
+ Xkey 25 usb keyboard (with built-in channel switching)
+ Waldorf Blofeld Synth (16 channels of multi-timbral goodness though this setup only uses 8 channels)
+ Akai MPC1000 (oldskool! Acting as sequencer/brain/laptop replacement running multi-timbral recording mode on JJOSXL)
+ iConnectivity mio 1x1 midi interface (converts midi din ports on mpc to usb for connecting to Pi)
+ DIY Arduino/Teensy Midi 6-button Foot Pedal (cause feet want to perform and manipulate mpc functions too)

## Workflow achieved
+ Keyboard midi notes can be played and route through MPC1000 and out to Blofeld for real-time synth performance.
+ Keyboard midi notes can be recorded into MPC1000 (mio usb midi cable) running JJOSXL as sequences.
+ MPC1000 midi sequences can play back out to Blofeld as backing tracks or performance where you manipulate blofeld knobs in real-time.
+ MPC1000 can record cc midi or knob movements from blofeld synth (note data filtered out to avoid bad midi loops from keyboard)
+ DIY Arduino/teensy foot pedal buttons each send midi cc values to mpc to control misc. performance functions with my feet in real-time.

![photo of hardware setup. waldorf blofeld synth module, akai mpc1000, iConnectivity mio 1x1 usb interface, Xkey 25 midi keyboard, TC Electronics Nova Delay, and Raspberry Pi 3](https://github.com/esaumusic/ding-pi/blob/master/images/IMG-3206.JPG)
