import rtmidi
import sys
import mymidi
import lights
import mididisplay

# range: 0 .. len(get_kights()) - 1
light_idx = 0

# v = 0 .. 100
def update_fader(fader, v, l):
    mididisplay.setLcdPanel(fader, f'{v}', l)
    v = int(v * 16383 / 100)
    msg = rtmidi.MidiMessage.pitchWheel(fader, v)
    mymidi.midiout().sendMessage(msg)

def update_faders():
    global light_idx
    light_list = lights.get_lights()
    i = 1
    for l in range(light_idx, light_idx + 8): # lights.get_lights():
        name = light_list[l]
        v = lights.get_light(name)
        update_fader(i, v, name)
        i = i + 1

def pageLeft(n):
    global light_idx
    if light_idx < n:
        light_idx = 0
    else:
        light_idx = light_idx - n
    update_faders()

def pageRight(n):
    global light_idx

    # If there's only 8 or fewer lights, can't move...
    l = len(lights.get_lights())
    if l <= 8:
        return
    light_idx = light_idx + n
    if light_idx + 8 >= l:
        light_idx = l - 8
    update_faders()


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
        m = mymidi.midiin().getMessage(100) # Timeout = 100
        if m:
            if m.isPitchWheel():
                c = m.getChannel()
                if c in range(1, 9):
                    v = m.getPitchWheelValue()
                    v = int(v * 100 / 16383)
                    l = lights.get_lights()[light_idx + c - 1]
                    update_fader(c, v, l)
                    lights.set_light(l, v, True)
            elif m.isNoteOn():
                if m.getNoteNumber() == 46:
                    pageLeft(8)
                elif m.getNoteNumber() == 47:
                    pageRight(8)
                elif m.getNoteNumber() == 48:
                    pageLeft(1)
                elif m.getNoteNumber() == 49:
                    pageRight(1)
                elif m.getNoteNumber() == 51:
                    lights.update_lights()
                    update_faders()

if __name__ == "__main__":
    sys.exit(main())
