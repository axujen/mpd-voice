#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

try:
	from mpd import MPDClient
except ImportError:
	print('You must install the python-mpd2 module. You can get it from:\n'\
			'https://pypi.python.org/pypi/python-mpd2')
	raise SystemExit
try:
	import pyttsx
except ImportError:
	print('You must install the pyttsx module. You can get it from:\n'\
			'https://pypi.python.org/pypi/pyttsx')
	raise SystemExit

class mpc(MPDClient):
    """MPD Client"""

    def __init__(self, server_id, vfemale, vrate, password=False):
        # Connect to the MPD server
        MPDClient.__init__(self)
        self.connect(**server_id)
        if password:
            self.password(password)

        # Initialize the pyttsx engine with its settings
        self.vengine = pyttsx.init("espeak", False)
        self.vengine.setProperty('rate', vrate)

        if vfemale:
            self.vengine.setProperty('voice', 'f4')
        else:
            self.vengine.setProperty('voice', 'm4')

        # Initialize lastsong variable
        self.lastsong=None

    def idleloop(self):
        """Wait untill a song changes then speak its title."""

        while True:
            self.idle('player') # wait for a signal from mpd

            # Skip if the music is not playing
            if not self.status()['state'] == 'play':
                continue

            # if the track actually changed
            if self.currentsong()["id"] != self.lastsong:
                self.speak(self.currentsong()["title"])
                self.lastsong = self.currentsong()["id"]

    def speak(self, string):
        """Speak the given string"""
        print(string)
        self.vengine.say(string)
        self.vengine.runAndWait()

    def __del__(self):
        self.close()
        self.disconnect()

def main():
    # Argument handling
    from argparse import ArgumentParser
    arguments = ArgumentParser(description="Speak mpd track changes with voice synthesis.")
    arguments.add_argument('-p', '--port', dest='port', default=6600, metavar='PORT',
            help='specify mpd\'s port (defaults to "6600")')
    arguments.add_argument('-u', '--host', dest='host', default='localhost', metavar='HOST',
            help='specify mpd\'s host (defaults to "localhost")')
    arguments.add_argument('--password', dest='password', default=None,metavar='PASSWORD',
            help='specify mpd\'s password')
    arguments.add_argument('-f', '--female', dest='vfemale', default=False, action='store_true',
            help='use a female voice instead of male.')
    arguments.add_argument('-r', '--rate', dest='vrate', default=150, type=int, metavar='VRATE',
            help='voice rate or speed, (defaults to "150")')
    args = arguments.parse_args()

    server_id={"host":args.host, "port":args.port}

    client = mpc(server_id, args.vfemale, args.vrate, args.password)
    client.idleloop()

if __name__ == '__main__':
    import sys
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
