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

from mpd import MPDClient
import pyttsx

class mpc(MPDClient):
    """MPD Client"""

    def __init__(self, server_id, password=False):
        # Connect to the MPD server
        MPDClient.__init__(self)
        self.connect(**server_id)
        if password:
            self.password(password)

        # Initialize the pyttsx engine
        self.vengine = pyttsx.init()

    def idleloop(self):
        """Just wait for the song to change"""

        while True:
            self.idle('player') # wait for song change
            self.speak(self.currentsong()["title"])


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
    args = arguments.parse_args()

    server_id={"host":args.host, "port":args.port}

    client = mpc(server_id, args.password)
    client.idleloop()

if __name__ == '__main__':
    main()
