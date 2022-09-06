import rtmidi
import sys

midi_in_device = None
midi_out_device = None

def midiinit():
    global midi_in_device
    global midi_out_device
    midi_in_device = rtmidi.RtMidiIn()
    midi_out_device = rtmidi.RtMidiOut()
    if len(sys.argv) < 2:
        print("Printing MIDI Ports")
        ports = range(midi_in_device.getPortCount())
        if ports:
            for i in ports:
                print("MIDI IN", midi_in_device.getPortName(i))
        ports = range(midi_out_device.getPortCount())
        if ports:
            for i in ports:
                print("MIDI OUT", midi_out_device.getPortName(i))
        return False
    midiPort = sys.argv[1]
    inret = False
    ports = range(midi_in_device.getPortCount())
    if ports:
        for i in ports:
            if midiPort == midi_in_device.getPortName(i):
                print("Opening MIDI IN", i)
                midi_in_device.openPort(i)
                inret = True
    outret = False
    ports = range(midi_out_device.getPortCount())
    if ports:
        for i in ports:
            if midiPort == midi_out_device.getPortName(i):
                print("Opening MIDI OUT", i)
                midi_out_device.openPort(i)
                outret = True

    if not inret:
        print("Unable to open MIDI IN")
        return False
    if not outret:
        print("Unable to open MIDI OUT")
        return False
    return True

def midiin():
    global midi_in_device
    return midi_in_device

def midiout():
    global midi_out_device
    return midi_out_device
