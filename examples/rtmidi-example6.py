import rtmidi
import sys

midiin = rtmidi.RtMidiIn()
midiout = rtmidi.RtMidiOut()

def print_message(midi):
    if midi.isNoteOn():
        print('ON: ', midi.getNoteNumber(), "=", midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity())
    elif midi.isNoteOff():
        print('OFF:', midi.getNoteNumber(), "=", midi.getMidiNoteName(midi.getNoteNumber()))
    elif midi.isController():
        print('CONTROLLER', midi.getControllerNumber(), midi.getControllerValue())
    elif midi.isChannelPressure():
        print('PRESSURE', midi.getChannelPressureValue())
    elif midi.isPitchWheel():
        print('PITCH WHEEL', midi.getChannel(), midi.getPitchWheelValue())
    else:
        print('SOMETHING ELSE!')
        
ports = range(midiout.getPortCount())
if ports:
    for i in ports:
        print("OUT ", midiout.getPortName(i))
    print("Opening port 0!")
    midiout.openPort(2)
    for i in range(0, 128):
        m2 = rtmidi.MidiMessage.controllerEvent(1, 75, i)
        ret = midiout.sendMessage(m2)
        print_message(m2)
        print("ret", ret, "Hit ENTER to continue")
        sys.stdin.read(1)
else:
    print('NO MIDI OUTPUT PORTS!')

ports = range(midiin.getPortCount())
if ports:
    for i in ports:
        print("IN ", midiin.getPortName(i))
    print("Opening port 0!") 
    midiin.openPort(0)
    while True:
        m = midiin.getMessage(250) # some timeout in ms
        if m:
            print_message(m)
            if m.isController():
                m2 = rtmidi.MidiMessage.controllerEvent(1, m.getControllerNumber() + 1, m.getControllerValue())
                midiout.sendMessage(m2)
            if m.isNoteOn() or m.isNoteOff():
                m2 = rtmidi.MidiMessage.noteOn(m.getChannel(), m.getNoteNumber(), m.getVelocity())
                midiout.sendMessage(m2)
else:
    print('NO MIDI INPUT PORTS!')
