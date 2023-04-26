import os
import subprocess

class RogueAP:
    def __init__(self, interface, essid, channel):
        self.interface = interface
        self.essid = essid
        self.channel = channel

    def create_ap(self):
        subprocess.run(["airbase-ng", "-e", self.essid, "-c", str(self.channel), "-v", self.interface], check=True)
