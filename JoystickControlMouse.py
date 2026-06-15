# Mouse Control via Arduino Joystick
# Reads joystick coordinates over serial, applies filtering and acceleration, then moves the mouse cursor.

import serial
import pyautogui
import math

# Disable PyAutoGUI safety delays for smoother real-time control
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

# Open serial connection to Arduino Nano
ser = serial.Serial('/dev/cu.usbserial-A50285BI', 250000)

# Calibrated joystick center position
CENTER_X = 507
CENTER_Y = 514

# Movement tuning parameters
DEADZONE = 35      # Ignore small joystick movements near center
MAX_SPEED = 15     # Maximum cursor movement speed

while True:
    try:
        # Read joystick coordinates from serial (format: x,y)
        line = ser.readline().decode().strip()
        x, y = map(int, line.split(','))

        # Convert raw values into offsets from center
        x -= CENTER_X
        y -= CENTER_Y

        # Apply deadzone filtering
        if abs(x) < DEADZONE:
            x = 0
        if abs(y) < DEADZONE:
            y = 0

        # Normalize joystick range to approximately -1.0 to 1.0
        nx = x / 512.0
        ny = y / 512.0

        # Apply non-linear acceleration curve for smoother control
        dx = math.copysign((abs(nx) ** 2.2) * MAX_SPEED, nx)
        dy = math.copysign((abs(ny) ** 2.2) * MAX_SPEED, ny)

        # Ignore extremely small cursor movements
        if abs(dx) < 0.15:
            dx = 0
        if abs(dy) < 0.15:
            dy = 0

        # Move cursor only when movement is required
        if dx != 0 or dy != 0:
            pyautogui.moveRel(dx, dy)

    # Silently ignore malformed serial data
    except:
        pass