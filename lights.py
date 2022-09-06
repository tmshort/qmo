from pythonosc.udp_client import SimpleUDPClient
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from typing import List, Any
import json
from natsort import natsorted
import threading

dispatcher = Dispatcher()
server = None
client = None

lights = dict()

def accept_anything(address: str, *osc_args: List[Any]) -> None:
    global lights
    if address[-17:] == "/lightCommandText":
        for i in osc_args:
            d = json.loads(i)
            d = d['data'].split('\n')
            for j in d:
                j = j.split(' = ')
                if j[1] == 'home':
                    j[1] = 0
                lights[j[0]] = int(j[1])

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

def update_lights():
    global lights
    global client
    global server
    client.send_message("/new", "light")
    client.send_message("/dashboard/recordAllToSelected", [])
    client.send_message("/cue/selected/lightCommandText", [])
    client.send_message("/delete/selected", [])
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

    
    
