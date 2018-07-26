# 07-23-18 - ESAU's DingPi Script (no this isn't chinese food, this turns your raspberry pi 3 into a midi usb host/router/midi processor by way of MidiDings!)
#
# Prerequisites:
# Raspberry Pi 3/3+ (other models untested but might work)
# Installed Raspbian Stretch Lite (https://www.raspberrypi.org/downloads/raspbian/)
# Installed alsa utilities (sudo apt-get install alsa-utils if connected to internet)
# Installed mididings (sudo apt-get install mididings if connected to internet)
# mididings documentation: http://dsacre.github.io/mididings/doc/start.html

# Reccomended:
# Wifi enabled for quick installation of prerequisites
# If you don't use linux much like me, enabling ssh on your pi so you can remote from another computer on your home network is pretty slick.
# Use linux utility crontab or equivalent to run this script on startup so you don't need a keyboard/monitorself. tutorial here: https://www.dexterindustries.com/howto/auto-run-python-programs-on-the-raspberry-pi/

# Overview of MIDI hardware involved:
# Xkey 25 usb keyboard (with built-in channel switching)
# Waldorf Blofeld Synth (16 channels of multi-timbral goodness though this setup only uses 8 channels)
# Akai MPC1000 (oldskool! Acting as sequencer/brain/laptop replacement running multi-timbral recording mode on JJOSXL)
# iConnectivity mio 1x1 midi interface (converts midi din ports on mpc to usb for connecting to Pi)
# DIY Arduino/Teensy Midi 6-button Foot Pedal (cause feet want to perform and manipulate mpc functions too)

# Workflow achieved:
# Keyboear midi notes can be played and route through mpc1000 and out to Blofeld for realtime synth performance.
# Keyboard midi notes can be recorded into MPC1000 (mio usb midi cable) running JJOSXL as sequences.
# MPC1000 midi sequences can play back out to Blofeld as backing tracks or performance where you manipulate blofeld knobs in real-time.
# MPC1000 can record cc midi or knob movements from blofeld synth (note data filtered out to avoid bad midi loops from keyboard)
# DIY Arduino/teensy foot pedal buttons each send midi cc values to mpc to control misc. performance functions with my feet in real-time.

from mididings import *

# config is mididings' setup function
config(
    # specify alsa as backend vs Jack which we're not using
    backend='alsa',

    # in_ports and out_ports will define and set up what I consider a virtual patchbay in that we set up all the backend connections with referenced names but don't interconnect them yet.
    # in_ports is all devices sending midi out via usb cable into raspberry pi for routing.
    # the first item in each set of parenthesis is arbitrary and can be named whatever you want. Second item is like an address and is specific to what [client]:[port] values are listed when you plug your gear into Pi and run aplaymidi -l command.
    in_ports = [
        ('blofeld out', 'Blofeld:0'),
        ('mio out', 'mio:0'),
        ('teensy out', 'Teensy MIDI:0'),
        ('xkey out', 'Xkey:0')
    ],
    # out_ports is all devices receiving midi data via usb cable outputted from raspberry pi.
    out_ports = [
        ('blofeld in', 'Blofeld:0'),
        ('mio in', 'mio:0')
    ]
)

# I consider this section the equivalent of virtual patch cables making connections on the virtual patchbay we declared above.
run(
    # routing channels individually from Xkey 25 key keyboard => mpc1000/mio => blofeld to enable multi-timbral playing, recording, playback,
    # also individually routing blofeld back to mpc100/mio for recording cc knob movements
    # PortSplit allows us to route individual input and output ports
    PortSplit({
        # here we duplicate keyboard midi 8 times, then filter each one to a specific channel and send to respective mio midi interface channel for multi-timbral capture into MPC1000 sequencer.
        'xkey out': [
            ChannelFilter(1) >> Output('mio in',1),
            ChannelFilter(2) >> Output('mio in',2),
            ChannelFilter(3) >> Output('mio in',3),
            ChannelFilter(4) >> Output('mio in',4),
            ChannelFilter(5) >> Output('mio in',5),
            ChannelFilter(6) >> Output('mio in',6),
            ChannelFilter(7) >> Output('mio in',7),
            ChannelFilter(8) >> Output('mio in',8)
        ],
        # with mpc correctly configured for multi-timbral, incoming midi passes thru to mpc midi out which we duplicate eight times here and filter/send out via mio midi interface to the blofeld midi in
        'mio out': [
            ChannelFilter(1) >> Output('blofeld in',1),
            ChannelFilter(2) >> Output('blofeld in',2),
            ChannelFilter(3) >> Output('blofeld in',3),
            ChannelFilter(4) >> Output('blofeld in',4),
            ChannelFilter(5) >> Output('blofeld in',5),
            ChannelFilter(6) >> Output('blofeld in',6),
            ChannelFilter(7) >> Output('blofeld in',7),
            ChannelFilter(8) >> Output('blofeld in',8)
        ],
        # Another duplication x 8, but this time from blofeld into mio/mpc. What's special here is KeyFilter(Lower=0) which is saying, "filter out all notes greater than or equal to 0" (in effect all notes!) which leaves us with just cc data.
        'blofeld out': [
            KeyFilter(lower=0) >> Output('mio in',1),
            KeyFilter(lower=0) >> Output('mio in',2),
            KeyFilter(lower=0) >> Output('mio in',3),
            KeyFilter(lower=0) >> Output('mio in',4),
            KeyFilter(lower=0) >> Output('mio in',5),
            KeyFilter(lower=0) >> Output('mio in',6),
            KeyFilter(lower=0) >> Output('mio in',7),
            KeyFilter(lower=0) >> Output('mio in',8)
        ],
        'teensy out': Output('mio in',1) # last but not least my diy arduino/teensy 6 button midi footswitch routed into mio/mpc to do something, not sure what yet but hey I had an extra usb port on the Pi so why not.
    })
)
