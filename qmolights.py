from pythonosc.udp_client import SimpleUDPClient
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from typing import List, Any
import json
from natsort import natsorted
import threading
import time
import rtmidi
import qmomidi

dispatcher = Dispatcher()
server = None
client = None

lights = dict()
light_update = 0

def accept_anything(address: str, *osc_args: List[Any]) -> None:
    global lights
    global light_update
    print(f"address={address}")
    if address[:18] == "/update/workspace/":
        if address[54:71] == "/cue_id/dashboard":
            cmd = address[54:] + "/children/shallow"
            print(f"cmd={cmd}")
            client.send_message(cmd, [])
    elif address[-17:] == "/lightCommandText":
        for i in osc_args:
            d = json.loads(i)
            d = d['data'].split('\n')
            for j in d:
                j = j.split(' = ')
                if j[1] == 'home':
                    j[1] = 0
                lights[j[0]] = int(j[1])
        light_update = light_update + 1

dispatcher.set_default_handler(accept_anything)

def get_lights():
    global lights
    return natsorted(list(lights.keys()))

def get_light(l):
    global lights
    return lights[l]

def set_light(l, v, send=False):
    global lights
    global client
    global server
    lights[l] = v
    print(f"set_light({l}, {v}, {send})")
    if send:
        client.send_message("/dashboard/setLight", [l, v])

def send_message(msg, args):
    client.send_message(msg, args)

def update_lights():
    global lights
    global client
    global light_update

    msg = rtmidi.MidiMessage.noteOn(1, 51, 127)
    qmomidi.midiout().sendMessage(msg)
    client.send_message("/new", "light")
    client.send_message("/dashboard/recordAllToSelected", [])
    client.send_message("/cue/selected/lightCommandText", [])
    client.send_message("/delete/selected", [])
    while light_update == 0:
        time.sleep(0.1)
    light_update = 0
    client.send_message("/updates", 1)
    client.send_message("/cueLists", [])
    msg = rtmidi.MidiMessage.noteOn(1, 51, 0)
    qmomidi.midiout().sendMessage(msg)
    print(get_lights())
    print(lights)


def osc_server():
    global server

    server = ThreadingOSCUDPServer(("127.0.0.1", 53001), dispatcher)
    print("starting OSC server")
    server.serve_forever()

def init_lights():
    global lights
    global server
    global client

    t = threading.Thread(target=osc_server)
    t.start()
    client = SimpleUDPClient("127.0.0.1", 53000)

    update_lights()
    print(lights)
