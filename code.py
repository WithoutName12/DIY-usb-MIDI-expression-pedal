from board import *
from analogio import AnalogIn
import time
from adafruit_midi.control_change import ControlChange
from adafruit_midi import MIDI
import usb_midi
from simpleio import map_range

# Initialise AnalogIn
pot = AnalogIn(A0)

# Initialise midi interface
midi = MIDI(midi_out=usb_midi.ports[1], out_channel=0)

# Initialise max and min values of potentiometer 
min_pot = 300
max_pot = 65535

# Calibration for first 10 seconds

start_time = time.monotonic()

while time.monotonic() - start_time <= 10:
    # Make variable value_pot first, because pot.value can change between if condition and initialisation
    value_pot = pot.value
    if value_pot < min_pot:
        min_pot = value_pot
    elif value_pot > max_pot:
        max_pot = value_pot

print(min_pot, max_pot)
# Delete start_time variable
del start_time

cc_value_sent = 0

while True:
    # Map pot values to 0-127
    cc_value = round(map_range(pot.value, min_pot, max_pot, 0, 127))
    print("CC_value: ", cc_value)
    time.sleep(0.05)
    # Check if value changed, and if it did only than send midi CC 
    if abs(cc_value - cc_value_sent) > 2:
        midi.send(ControlChange(4, cc_value))
        cc_value_sent = cc_value