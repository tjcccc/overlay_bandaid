# OverlayBandaid

## What is it

Some games running in Linux with Gamescope may experience stuck or freeze issues, and errors in the console will be like:

```bash
[gamescope] [Error] xdg_backend: Compositor released us but we were not acquired. Oh no.
[gamescope] [Error] xdg_backend: Compositor released us but we were not acquired. Oh no.
[gamescope] [Error] xdg_backend: Compositor released us but we were not acquired. Oh no.
```

I found that putting an app window over the game screen. Those games will be unfrozen and work as usual.

ChatGPT said the reason is that the overlay window will let the game leave the direct scanout mode. So, I made this workaround app with ChatGPT's help.

## Usage

Just run the built bin, and a semi-transparent tiny window (32 * 16) will show up.

You can move it to any place on the screen.

How to quit? Right-click on it and select `Quit`. 

## Build with Nuitka

```bash
nuitka --onefile --standalone --enable-plugin=pyqt6 --output-filename=OverlayBandAid main.py
```