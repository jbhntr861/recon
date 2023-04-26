import os
import subprocess

class HTTrack:
    def __init__(self, url, output_dir):
        self.url = url
        self.output_dir = output_dir

    def download_website(self):
        subprocess.run(["httrack", self.url, "-O", self.output_dir, f"+*.{self.url.split('.')[1]}/*"], check=True)
