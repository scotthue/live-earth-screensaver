# live-earth-screensaver

There's a satellite called Himawari-8 which is geostationary over approximately Papua New Guinea. The very excellent people who run this satellite have set up a [live stream](http://himawari8.nict.go.jp/) of the ultra-high-res images that it takes. They are gorgeous.

Inspired by [someone awesome on Reddit](https://www.reddit.com/r/programming/comments/441do9/i_made_a_windows_powershell_script_that_puts_a/), and based on a script by [celoyd](https://github.com/celoyd), I built a script that downloads a recent photo. This is forked from [willwhitney](https://github.com/willwhitney/live-earth-desktop). It downloads a slightly older (16 hours) image so that the sunlight on the earth matches with a Chicago timezone (plus or minus one hour), even if the image is taken over Asia Pacific. With a `plist` file for `launchd` on OS X, I can run this script every ten minutes and always have the latest image on my machine. And then by setting my OS X screensaver to a slideshow of the images inside a folder, the latest Himawari-8 photo is always set as my screensaver image.

![](example.png)

## Instructions

1. Clone this repo
2. If you don't have PIL or Pillow installed, `pip install Pillow`
3. If you don't have the requests module installed, `pip install requests`
3. Change the paths set in `himawari.plist` to paths inside this directory, and update your path to python if need be.
4. Try the Python script by running `python himawari.py` just to make sure everything's kosher. It should download an image.
5. `ln -s <this-dir>/himawari.plist /Users/<you>/Library/LaunchAgents/`
6. `launchctl load -w /Users/<you>/Library/LaunchAgents/himawari.plist` to start it running every 10 minutes
7. Go to OS X Preferences > Desktop and Screen Saver and set your screensaver to rotate through the images contained in the `images` directory that you're writing these images to (whatever directory you made `out` point to).
8. Enjoy!
