import os
import eel
from engine.features import *
from engine.command import *
from engine.auth import recoganize
def start():


    eel.init("www")

    playAssistantSound()

    @eel.expose
    def init():
        flag = recoganize.AuthenticateFace()
        eel.hideStart()
        playAssistantSound()


    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    eel.start('index.html',mode=None,host='localhost',block=True)