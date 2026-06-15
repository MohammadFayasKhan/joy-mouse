<div align="center">

# 🕹️ Joy Mouse

### *Transform a joystick into a precision desktop pointing device*

[![Arduino](https://img.shields.io/badge/Arduino-Nano-00979D?style=for-the-badge&logo=arduino&logoColor=white)](https://www.arduino.cc/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PySerial](https://img.shields.io/badge/PySerial-Serial_IO-4B8BBE?style=for-the-badge)](https://pyserial.readthedocs.io/)
[![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-Mouse_Control-FF6B35?style=for-the-badge)](https://pyautogui.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/Version-v1.0_Wired-blueviolet?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)]()

<br/>

![Joy Mouse Project](Pic.PNG)

<br/>

> **Built for learning, experimentation, and embedded systems exploration.**

</div>

---

## 📖 Project Overview

**Joy Mouse** bridges the gap between hardware and software — turning a simple analog joystick module and an Arduino Nano into a fully functional desktop mouse controller. Joystick position data is streamed over USB serial at high speed, then interpreted by a Python script that applies **deadzone filtering**, **center calibration**, and a **non-linear acceleration curve** to produce smooth, responsive cursor movement.

Whether you're exploring embedded systems, building an accessibility device, or simply experimenting with hardware-software integration, Joy Mouse is a clean, well-structured starting point.

---

## ✨ Features

### 🔌 Current — v1.0 Wired Edition

| Feature | Description |
|---|---|
| 🖱️ **Wired Joystick Control** | Full X/Y axis cursor control via USB serial |
| ⚡ **High-Speed Serial** | 250,000 baud rate for near-zero latency |
| 🎯 **Deadzone Filtering** | Eliminates cursor drift from joystick jitter |
| 📐 **Center Calibration** | Automatically maps joystick center to rest state |
| 🚀 **Adaptive Acceleration** | Non-linear (power 2.2) curve for precision at low speed, speed at high displacement |
| 🧹 **Lightweight Python** | Minimal dependencies, clean & readable code |
| 🔧 **Arduino Nano Based** | Compact, affordable, and beginner-friendly |

---

## 🗺️ Future Roadmap

```
v1.0  ██████████  Wired Edition          ✅ Released
v2.0  ░░░░░░░░░░  Wi-Fi Edition          🔜 Planned
v3.0  ░░░░░░░░░░  Bluetooth Edition      🔜 Planned
v4.0  ░░░░░░░░░░  Gesture Control        🔜 Planned
```

| Version | Feature | Status |
|---|---|---|
| **v1.0** | Wired USB joystick control | ✅ **Released** |
| **v2.0** | Wi-Fi mouse control (ESP8266/ESP32) | 🔜 Planned |
| **v3.0** | Bluetooth mouse control (BLE HID) | 🔜 Planned |
| **v4.0** | Gesture-based control (IMU/Camera) | 🔜 Planned |
| **v4.x** | Mobile companion app | 🔜 Planned |
| **v4.x** | Multi-device support | 🔜 Planned |
| **v4.x** | Custom sensitivity profiles | 🔜 Planned |
| **v4.x** | Battery-powered portable version | 🔜 Planned |

---

## 🛠️ Hardware Required

| Component | Purpose |
|---|---|
| 🔵 **Arduino Nano** | Microcontroller — reads joystick & streams serial data |
| 🕹️ **Analog Joystick Module** | 2-axis input (X/Y), produces 0–1023 analog values |
| 🧪 **Breadboard** | Prototyping — no soldering required |
| 🔌 **Jumper Wires** | Connecting joystick to Arduino Nano pins |
| 🔋 **USB Cable** | Powers the Arduino and provides serial communication |

---

## 💻 Software Requirements

| Software | Version | Purpose |
|---|---|---|
| 🐍 **Python** | 3.x | Runtime for the mouse controller script |
| 📡 **PySerial** | Latest | Serial communication with Arduino |
| 🖱️ **PyAutoGUI** | Latest | Cross-platform cursor movement control |
| ⚙️ **Arduino IDE** | 1.x / 2.x | Compiling and uploading the `.ino` sketch |

Install Python dependencies with:

```bash
pip install pyserial pyautogui
```

---

## 📁 Project Structure

```
JoystickMouse/
│
├── 📄 JoystickMouse.ino          # Arduino sketch — reads joystick & sends serial data
├── 🐍 JoystickControlMouse.py    # Python script — receives data & controls cursor
├── 🖼️  Pic.PNG                    # Project hero image
├── 🖼️  code.png                   # Code screenshot / reference image
├── 📄 .gitignore                  # Python & Arduino gitignore rules
└── 📄 README.md                  # This file
```

---

## ⚙️ Arduino Code

**File:** `JoystickMouse.ino`

The Arduino sketch reads raw analog values from the joystick's X and Y axes every 5 ms and transmits them over serial in `x,y` format at 250,000 baud.

```cpp
// Arduino Nano Joystick Reader
// Reads analog joystick X/Y positions and sends them over Serial for mouse control.

const int VRX = A0; // Joystick X-axis pin
const int VRY = A1; // Joystick Y-axis pin

void setup() {
  // Initialize high-speed serial communication
  Serial.begin(250000);
}

void loop() {
  // Read joystick axis values (0–1023)
  int x = analogRead(VRX);
  int y = analogRead(VRY);

  // Send data in "x,y" format
  Serial.print(x);
  Serial.print(",");
  Serial.println(y);

  // Small delay for stable and responsive updates
  delay(5);
}
```

**Key Details:**
- Baud rate: `250000` — high-speed for minimal latency
- Output format: `x,y\n` (e.g., `507,514`)
- Loop interval: 5 ms → ~200 readings/second

---

## 🐍 Python Code

**File:** `JoystickControlMouse.py`

The Python script opens the serial port, reads the joystick stream, and translates axis values into cursor movement using filtering and acceleration logic.

```python
# Mouse Control via Arduino Joystick
# Reads joystick coordinates over serial, applies filtering and acceleration,
# then moves the mouse cursor.

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

    except:
        pass
```

---

## 🔌 Circuit Connections

Wire the joystick module to the Arduino Nano as follows:

| Joystick Pin | Arduino Nano Pin | Description |
|---|---|---|
| `VCC` | `5V` | Power supply |
| `GND` | `GND` | Ground |
| `VRX` | `A0` | X-axis analog output |
| `VRY` | `A1` | Y-axis analog output |
| `SW` | *(Not connected)* | Button switch (optional) |

> 💡 **Tip:** The joystick's `SW` (switch) pin can be connected to a digital pin (e.g., `D2`) for click functionality in future versions.

---

## 🚀 Installation Guide

### Step 1 — Clone the Repository

```bash
git clone https://github.com/MohammadFayasKhan/joy-mouse.git
cd joy-mouse
```

### Step 2 — Install Python Dependencies

```bash
pip install pyserial pyautogui
```

### Step 3 — Flash the Arduino

1. Open **Arduino IDE**
2. Open `JoystickMouse.ino`
3. Select **Board:** `Arduino Nano`
4. Select **Processor:** `ATmega328P` (or `ATmega328P Old Bootloader` if needed)
5. Select the correct **Port** under `Tools > Port`
6. Click **Upload** ✅

### Step 4 — Find Your Serial Port

**macOS / Linux:**
```bash
ls /dev/cu.*        # macOS
ls /dev/tty*        # Linux
```

**Windows:**
```
Device Manager → Ports (COM & LPT) → Look for "USB Serial Device"
```

### Step 5 — Configure the Python Script

Open `JoystickControlMouse.py` and update the serial port:

```python
# Replace with your actual port:
ser = serial.Serial('/dev/cu.usbserial-XXXXXXXX', 250000)
#                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                    macOS example: /dev/cu.usbserial-A50285BI
#                    Linux example: /dev/ttyUSB0
#                    Windows:       COM3
```

---

## ▶️ Usage Guide

### Step 1 — Connect the Hardware
Plug in the Arduino Nano via USB. Ensure the joystick is wired correctly per the circuit table above.

### Step 2 — Run the Python Controller
```bash
python JoystickControlMouse.py
```

### Step 3 — Control the Cursor
- Move the joystick in any direction → cursor moves accordingly
- Return joystick to center → cursor stops (deadzone prevents drift)
- Push further from center → cursor accelerates (adaptive curve)

### Step 4 — Stop the Script
Press `Ctrl + C` in the terminal to stop.

> ⚠️ **Note:** `pyautogui.FAILSAFE` is disabled in this script. Move your mouse to a screen corner to force-stop if needed, or use `Ctrl + C`.

---

## 🧠 How It Works

### 1. 📡 Serial Communication
The Arduino reads the joystick 200 times per second and sends `x,y` pairs over USB at 250,000 baud. Python reads each line using `ser.readline()`.

### 2. 🎯 Center Calibration
Raw joystick values are offset by the calibrated center (`CENTER_X = 507`, `CENTER_Y = 514`), converting absolute readings into directional deltas.

### 3. 🔇 Deadzone Filtering
Any delta within ±35 units of center is clamped to zero. This eliminates cursor drift caused by joystick mechanical jitter when the stick is at rest.

### 4. 🚀 Dynamic Acceleration
The normalized offset is raised to the power of **2.2**, creating a non-linear acceleration curve:
- **Slight nudge** → very slow, precise movement
- **Full displacement** → fast, sweeping movement

```
speed = |offset|^2.2 × MAX_SPEED
```

### 5. 🖱️ Cursor Movement
`pyautogui.moveRel(dx, dy)` moves the cursor relative to its current position. Movements below 0.15 pixels are suppressed to avoid sub-pixel jitter.

---

## 🏷️ Version Information

| Version | Name | Status | Key Feature |
|---|---|---|---|
| **v1.0** | 🔌 Wired Edition | ✅ Current | USB joystick via PySerial |
| **v2.0** | 📶 Wi-Fi Edition | 🔜 Planned | ESP8266/ESP32 wireless |
| **v3.0** | 📲 Bluetooth Edition | 🔜 Planned | BLE HID protocol |
| **v4.0** | 🖐️ Gesture Edition | 🔜 Planned | IMU / camera gestures |

---

## 📸 Screenshots

<div align="center">

**Project Hardware — Arduino Nano & Joystick on Breadboard**

![Joy Mouse Hardware](Pic.PNG)

<br/>

**Code Reference**

![Joy Mouse Code](code.png)

</div>

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature-name`
3. **Commit** your changes: `git commit -m 'feat: add your feature'`
4. **Push** to your branch: `git push origin feature/your-feature-name`
5. **Open** a Pull Request

### Contribution Ideas
- 🖱️ Add left/right click support using the joystick button (`SW` pin)
- 📜 Implement scroll wheel simulation
- ⚙️ Add a config file for port, deadzone, and speed settings
- 📶 Implement v2.0 Wi-Fi communication via ESP32

Please keep code clean, commented, and consistent with the existing style.

---

## 📄 License

This project is licensed under the **MIT License** — you are free to use, modify, and distribute it for personal and commercial purposes.

See the [LICENSE](LICENSE) file for full details.

---

## 👤 Author

<div align="center">

### Mohammad Fayas Khan

[![GitHub](https://img.shields.io/badge/GitHub-MohammadFayasKhan-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/MohammadFayasKhan)
[![Repository](https://img.shields.io/badge/Repo-joy--mouse-blueviolet?style=for-the-badge&logo=github)](https://github.com/MohammadFayasKhan/joy-mouse)

*"Built for learning, experimentation, and embedded systems exploration."*

</div>

---

<div align="center">

**⭐ If you found this project useful, please give it a star on GitHub! ⭐**

Made with ❤️ by [Mohammad Fayas Khan](https://github.com/MohammadFayasKhan)

</div>
