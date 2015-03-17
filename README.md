mpd-voice
============
Notification for mpd track changes using voice synthesis

#Usage
```
usage: mpd-voice.py [-h] [-p PORT] [-u HOST] [--password PASSWORD] [-f]
                    [-r VRATE]

Speak mpd track changes with voice synthesis.

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  specify mpd's port (defaults to "6600")
  -u HOST, --host HOST  specify mpd's host (defaults to "localhost")
  --password PASSWORD   specify mpd's password
  -f, --female          use a female voice instead of male.
  -r VRATE, --rate VRATE
                        voice rate or speed, (defaults to "150")
```
