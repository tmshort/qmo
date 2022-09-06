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
    elif midi.isSysEx():
        print("SYS EX", midi.getRawData())
    else:
        print('SOMETHING ELSE!')
        
ports = range(midiout.getPortCount())
if ports:
    for i in ports:
        print("OUT ", midiout.getPortName(i))
    print("Opening port 0!")
    midiout.openPort(0)
    #msg = [ 0x0, 0x0, 0x66, 0x58, 0x20, 0x41, 0x43, 0x68, 0x20, 0x31, 0x0, 0x0, 0x0, 0x20, 0x20, 0x20, 0x20, 0x61, 0x42, 0x33 ]
    msg = [ 0x0, 0x0, 0x66, 0x14, 0x12, 0x38, 0x43, 0x68, 0x20, 0x31 ]
    m2 = rtmidi.MidiMessage.createSysExMessage(bytes(msg))
    ret = midiout.sendMessage(m2)
    print_message(m2)

    msg = [ 0x0, 0x0, 0x66, 0x14, 0x12, 0x0, 0x43, 0x68, 0x20, 0x32 ]
    m2 = rtmidi.MidiMessage.createSysExMessage(bytes(msg))
    ret = midiout.sendMessage(m2)
    print_message(m2)

    msg = [ 0x0, 0x0, 0x66, 0x14, 0x12, 0x10, 0x43, 0x68, 0x20, 0x33 ]
    m2 = rtmidi.MidiMessage.createSysExMessage(bytes(msg))
    ret = midiout.sendMessage(m2)
    print_message(m2)

    msg = [ 0x0, 0x0, 0x66, 0x14, 0x12, 0x37, 0x43, 0x68, 0x20, 0x34 ]
    m2 = rtmidi.MidiMessage.createSysExMessage(bytes(msg))
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
