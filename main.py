import rtmidi
import sys
import mymidi
import lights
import mididisplay

# v = 0 .. 100
def update_fader(fader, v, l):
    mididisplay.setLcdPanel(fader, f'{v}', l)
    v = int(v * 16383 / 100)
    msg = rtmidi.MidiMessage.pitchWheel(fader, v)
    mymidi.midiout().sendMessage(msg)

def update_faders():
    i = 1
    for l in lights.get_lights():
        if (i <= 8):
            v = lights.get_light(l)
            update_fader(i, v, l)
            i = i + 1

def main():
    if not mymidi.midiinit():
        return 0

    lights.init_lights()

    # indicate QLAB mode!
    mididisplay.setBars("qla")
    mididisplay.setBeats("b ")

    # Get the first 8 lights
    update_faders()
    
    while True:
        print("getMessage()")
        m = mymidi.midiin().getMessage(100) # Timeout = 100
        if m:
            if m.isPitchWheel():
                c = m.getChannel()
                v = m.getPitchWheelValue()
                v = int(v * 100 / 16383)
                l = lights.get_lights()[c-1]
                update_fader(c, v, l)
                lights.set_light(l, v, True)
            # if pitch wheel (i.e. fader) send back to keep it at position
            # send message via OSC
            # Log message?
        #print("update_lights()")
        #lights.update_lights()
        #print("update_faders()")
        #update_faders()
    

if __name__ == "__main__":
    sys.exit(main())
