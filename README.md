# Hand Gesture Mouse

A first attempt at implementing computer vision.

Control your computer's mouse with your hand using your webcam.
Point with your index finger to move the cursor, and pinch your
thumb and index finger together to click.

Built with Python, OpenCV, MediaPipe and PyAutoGUI.

## Files

- `mouse-control.py`: the hand gesture mouse
- `main.py`: a simpler demo that just tracks and draws your hand

## Setup

Requires **Python 3.12** (newer versions don't work with this version of MediaPipe).

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run it

```bash
python mouse-control.py
```

Press **Q** in the camera window to quit.

## Mac permissions

In System Settings → Privacy & Security, give the app you're running it from
(e.g. VS Code or Terminal) access to:

- **Camera**: so it can see your hand
- **Accessibility**: so it can move and click the mouse

Restart that app after turning these on.

## Tuning

At the top of `mouse-control.py`:

- `smoothing`: lower = smoother but slower cursor, higher = faster but shakier
- `pinch_threshold`: how close your fingers need to be to count as a click