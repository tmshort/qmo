import rtmidi
import mymidi
# These set the text in the 7-segment-display area. |raw=True| means to use the
# raw data to get odd characters, otherwise, text is translated as best
# as I can

def translateTextToMcu(text):
    """Convert ASCII text into Mackie's seven-segment display text"""
    newtext = list()
    for c in text:
        if c.isupper():
            newtext.append(ord(c) - ord('A') + 1)
        elif c.islower():
            newtext.append(ord(c) - ord('a') + 1)
        elif c.isdigit():
            newtext.append(ord(c) - ord('0') + 48)
        elif c.isspace():
            newtext.append(0)
        elif c == '.' and len(newtext) > 0 and newtext[-1] < 64:
            newtext[-1] = newtext[-1] + 64
        elif c == '-':
            newtext.append(45)
        elif c == '_':
            newtext.append(46)
    return newtext

def doSevenSegment(position, value):
    msg = rtmidi.MidiMessage.controllerEvent(1, position, value)
    mymidi.midiout().sendMessage(msg)

def setAssignment(text, raw=False):
    if len(text) == 0:
        return
    if raw == False:
        text = translateTextTo7SD(text)
    else:
        text = bytes(text)
    if len(text) > 0:
        doSevenSegment(75, text[0])
    else:
        doSevenSegment(75, 0)
    if len(text) > 1:
        doSevenSegment(74, text[1])
    else:
        doSevenSegment(74, 0)

def setBars(text, raw=False):
    if len(text) == 0:
        return
    if raw == False:
        text = translateTextToMcu(text)
    else:
        text = bytes(text)
    if len(text) > 0:
        doSevenSegment(73, text[0])
    else:
        doSevenSegment(73, 0)
    if len(text) > 1:
        doSevenSegment(72, text[1])
    else:
        doSevenSegment(72, 0)
    if len(text) > 2:
        doSevenSegment(71, text[2])
    else:
        doSevenSegment(71, 0)

def setBeats(text, raw=False):
    if len(text) == 0:
        return
    if raw == False:
        text = translateTextToMcu(text)
    text = bytes(text)
    if len(text) > 0:
        doSevenSegment(70, text[0])
    else:
        doSevenSegment(70, 0)
    if len(text) > 1:
        doSevenSegment(69, text[1])
    else:
        doSevenSegment(69, 0)

def setSubDivision(text, raw=False):
    if len(text) == 0:
        return
    if raw == False:
        text = translateTextToMcu(text)
    else:
        text = bytes(text)
    if len(text) > 0:
        doSevenSegment(68, text[0])
    else:
        doSevenSegment(68, 0)
    if len(text) > 1:
        doSevenSegment(67, teext[1])
    else:
        doSevenSegment(67, 0)

def setTicks(text, raw=False):
    if len(text) == 0:
        return
    if raw == False:
        text = translateTextToMcu(text)
    else:
        text = bytes(text)
    if len(text) > 0:
        doSevenSegment(66, text[0])
    else:
        doSevenSegment(66, 0)
    if len(text) > 1:
        doSevenSegment(65, text[1])
    else:
        doSevenSegment(65, 0)
    if len(text) > 2:
        doSevenSegment(64, text[2])
    else:
        doSevenSegment(64, 0)

# Sets the text over the whole LCD display, starting at |startpos|
def setLcdRaw(text, startpos=0):
    command = [ 0x00, 0x00, 0x66, 0x14 ] # SysEx without xF0
    command.append(0x12) # LCD
    command.append(startpos)

    max = 112 - startpos
    if len(text) > max:
        text = text[:max]
    
    for c in text:
        command.append(ord(c))

    # Don't bother with xF7 terminator
    msg = rtmidi.MidiMessage.createSysExMessage(bytes(command))
    mymidi.midiout().sendMessage(msg)

# Sets the text over the whole LCD display, starting at |row, column|
# This is basically a broken out setLcdRaw()
def setLcdRC(text, row=0, column=0):
    setLcdRaw(text, row * 0x38 + column)

# Sets the text for a single LCD Panel, with |panel| from 1 to 8
def setLcdPanel(panel, textTop='', textBottom=''):
    posTop = (panel - 1) * 7
    posBottom = posTop + 0x38

    if len(textTop) > 7:
        textTop = textTop[:7]
    else:
        while len(textTop) < 7:
            textTop = textTop + ' '

    if len(textBottom) > 7:
        textBottom = textBottom[:7]
    else:
        while len(textBottom) < 7:
            textBottom = textBottom + ' '

    setLcdRaw(textTop, posTop)
    setLcdRaw(textBottom, posBottom)

if __name__ == "__main__":
    setLcdPanel(1, 'Hello', 'World')
    setLcdPanel(1, 'Hello12345', 'World67890')
    setTicks("12")
    setTicks("1.2")
    setTicks("AB")
    setTicks(b'\x00\x01\x02', True)
    
