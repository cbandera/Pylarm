#    Copyright 2015 Claudio Bandera
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#

from time import sleep
import subprocess
import pygame
import click
import sys
import os

this_dir = os.path.dirname(__file__)
audio_file = os.path.join(this_dir, "resources", "Ping-da-ding-ding-ding.ogg")
icon_path = os.path.join(this_dir, 'resources', 'icon.png')


class Timer:
    def __init__(self, duration, msg):
        self.duration = duration
        self.msg = msg

    def start(self):
        try:
            sleep(self.duration)
            self.notify()
            self.alarm()
        except KeyboardInterrupt:
            print "Interrupted by user"
            sys.exit(1)

    @staticmethod
    def alarm():
        pygame.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pass

    def notify(self):
        try:
            executable = subprocess.check_output('which notify-send', shell=True)[:-1]
        except subprocess.CalledProcessError:
            return
        subprocess.Popen([executable, '-i', icon_path, '-t', '2000', '--hint', 'int:transient:1', "Pylarm", self.msg],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)


@click.command()
@click.option('--seconds', '-s', default=0, help='Specify a duration in seconds.', type=click.INT)
@click.option('--minutes', '-m', default=0, help='Specify a duration in minutes.', type=click.INT)
@click.option('--hours', '-h', default=0, help='Specify a duration in hours.', type=click.INT)
@click.argument("message", default="Wake up", type=click.STRING)
def main(seconds, minutes, hours, message):
    """A small command line alarm utility written in Python"""
    duration = (hours * 60 + minutes) * 60 + seconds
    timer = Timer(duration, message)

    click.echo("Starting Timer with {} seconds".format(duration))
    timer.start()
