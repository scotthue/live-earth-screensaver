import requests
import sys
from datetime import datetime, timedelta
import pytz
from PIL import Image
from StringIO import StringIO
import os
import logging
import uuid

# python himawari.py
# stolen from https://gist.github.com/celoyd/39c53f824daef7d363db
# requires speedtest-cli ('pip install speedtest-cli')

# Fetch Himawari-8 full disks at a given zoom level and set as desktop.
# Valid zoom levels seem to be powers of 2, 1..16, and 20.
#
# To do:
# - Librarify.
# - Clean up this paths business
# - Install script

script_dir = os.path.dirname(os.path.realpath(__file__))

print("Checking internet speed:")

def ping():
    import re
    import subprocess
    try:
        ping_out = subprocess.check_output("ping -c 5 google.com | tail -1", shell=True)
        matcher = re.compile("round-trip min/avg/max/stddev = (\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)")
        return float(matcher.search(ping_out).group(1))
    except Exception as ex:
        print "Problem with internet connection. Quitting..."
        os._exit(1)

ping = ping()
print("Ping: " + str(ping) + " ms")

if (ping > 200): # We require ping to be under 200 ms as a basic test
    print "Latency (ping) is too high. Quitting..."
    os._exit(1)
else:
    print "Internet connection is ok."

def speedtest():
    import json
    import subprocess
    try:
        speedtest = subprocess.check_output("speedtest-cli --json", shell=True)   
        data = json.loads(speedtest)
        return data["download"]
    except Exception as ex:
        print "Problem with speedtest. Quitting..."
        os._exit(1) 

speed = speedtest()

print("Download speed: ~" + str(speed//1000000) + " Mb/s")

if (speed > 5000000): # 5 Mb/s
    print "Internet speed is good. Downloading hi-res image."
    scale = 8
elif (speed > 1000000): # 1 Mb/s
    print "Internet speed is ok. Downloading medium-res image."
    scale = 4
else:
    print "Internet speed is poor. Quitting..."
    os._exit(1)

# Tile size for this dataset:
width = 550
height = 550

tz = pytz.timezone('UTC')

# they don't get uploaded immediately. 40 minutes is a conservative delay.
time = datetime.now(tz) - timedelta(minutes=400)
print("Fetching image for time: " + datetime.strftime(time, "%Y-%m-%d %H:%M:%S"))
# set these appropriately for yourself
# using a UUID just so the OS sees a new filename each time it goes to change
#   the desktop image. if it's always the same name, it won't change
tmp = script_dir + '/tmp.png'
out = script_dir + '/desktop-%s.png' % (str(uuid.uuid4()))


base = 'http://himawari8.nict.go.jp/img/D531106/%sd/550' % (scale)

tiles = [[None] * scale] * scale

def pathfor(t, x, y):
    return "%s/%s/%02d/%02d/%02d%02d00_%s_%s.png" \
    % (base, t.year, t.month, t.day, t.hour, (t.minute / 10) * 10, x, y)


sess = requests.Session() # so requests will reuse the connection
png = Image.new('RGB', (width*scale, height*scale))

def fetch_and_set():
    previous_tiledata = ""
    for x in range(scale):
        for y in range(scale):
            path = pathfor(time, x, y)
            tiledata = sess.get(path).content

            # we're just getting the "No Image" image
            # no need to retry, there just isn't data for right now
            if tiledata == previous_tiledata:
                print("No image available, quitting.")
                sys.exit(0)

            tile = Image.open(StringIO(tiledata))
            png.paste(tile, (width*x, height*y, width*(x+1), height*(y+1)))

    png.save(tmp, 'PNG')

    # clear out the old images in this folder so the OS picks the right one
    os.system("rm " + script_dir + "/images/*")

    # now move in the new image. doing it like this because writing the image
    # takes a while, so it's better to make it a (semi-) atomic swap
    os.system("mv %s %s" % (tmp, out))


try:
    fetch_and_set()
except requests.exceptions.ConnectionError:
    logging.exception('')

    # a very dirty try-at-most-twice
    try:
        fetch_and_set()
    except requests.exceptions.ConnectionError:
        logging.exception('')
