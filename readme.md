# live-earth-screensaver

There's a satellite called Himawari-8 which is geostationary over approximately Papua New Guinea. The very excellent people who run this satellite have set up a [live stream](http://himawari8.nict.go.jp/) of the ultra-high-res images that it takes. They are gorgeous.

Inspired by [someone awesome on Reddit](https://www.reddit.com/r/programming/comments/441do9/i_made_a_windows_powershell_script_that_puts_a/), and based on a script by [celoyd](https://github.com/celoyd), I built a script that downloads a recent photo. This is forked from [willwhitney](https://github.com/willwhitney/live-earth-desktop). It downloads a slightly older (16 hours) image so that the sunlight on the earth matches with a Chicago timezone (plus or minus one hour), even if the image is taken over Asia Pacific. Before downloading, the script does some tests on the internet speed of the device using `speedtest-cli`, after which we decide to download the hi-res image (5 Mb/s+ connections), medium-res image (1-5 Mb/s connections), or no image (for slower connections). Using the `crontab` on OS X, I can run this script every ten minutes and always have the latest image on my machine. And then by setting my OS X screensaver to a slideshow of the images inside a folder, the latest Himawari-8 photo is always set as my screensaver image.

![](example.png)

## Instructions

1. Clone this repo and enter directory: `git clone https://github.com/scotthue/live-earth-screensaver.git && cd live-earth-screensaver`
2. Install dependencies as needed (see below), sudo may be require for some or all
3. Make output directory: `mkdir images`
3. Create blank log files: `touch out.log err.log`
4. Try the Python script by running `python himawari.py` just to make sure everything's kosher. It should download an image.
5. Edit your crontab (see below)
7. Go to OS X Preferences > Desktop and Screen Saver and set your screensaver to rotate through the images contained in the `images` directory that you're writing these images to (whatever directory you made `out` point to).
8. Enjoy!

### Dependencies
* Python 2.7 or greater.
* PIP: `sudo easy_install pip`
* PIL or Pillow: `pip install Pillow`
* Requests module: `pip install requests`
* Speedtest-cli: `pip install speedtest-cli`
* Default OS X `ping` (if you have something else, you will have to update the script)

### Crontab
Add this to the beginning your crontab (with `crontab -e`), *updating the path of the script and python path as needed*:
```shell
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

*/10 * * * * cd ~/git-projects/live-earth-screensaver/ && /usr/bin/python himawari.py >out.log 2>err.log
```

If your crontab already has `SHELL` and `PATH` defined, update them as appropriate.
