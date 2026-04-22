Author - Daksh Fofindi (Daksh Aerospace)

# If you liked my work please follow me on below social media profiles

youtube - https://m.youtube.com/@dakshfofindi907/videos?view=0&sort=dd&shelf_id=2
<br>
Website - http://www.dakshaerospace.in/
<br>
instagram - https://www.instagram.com/dakshfofindi/
<br>
X - https://x.com/dakshfofindi
<br>
LinkedIn - https://in.linkedin.com/in/dakshfofindi

---

Note: Change com port accrding to your hardware.
---

# S.P.H.E.R.E. Rocket Ground Station

A real-time telemetry visualization system for rocket avionics, built using Python, PyQt6, and PyQtGraph.

This ground station receives live data from the flight computer via serial communication and displays it through an interactive GUI for monitoring and analysis.

---

## Overview

This project is part of a complete **rocket telemetry system**, where:

- ESP32 sends flight data
- Ground station receives & visualizes data in real time
- Engineers monitor flight parameters live

---

## Tech Stack

- Python 3
- PyQt6 (GUI Framework)
- PyQtGraph (Real-time plotting)
- PySerial (Serial communication)

---

## Features

- Real-time plotting (Altitude, Temperature, Pressure, RSSI)
- Acceleration & Gyroscope visualization (X, Y, Z axes)
- Live RF telemetry monitoring (RSSI, SNR, Frequency Error)
- Mission time tracking
- Moving average indicators
- RF Link status indicator
- Fast update loop (50ms)

---

## Telemetry Data Format

```csv
Packet,Interval,Size,
Temp,Pressure,Altitude,
AccX,AccY,AccZ,
GyroX,GyroY,GyroZ,
RSSI,SNR,FreqError

---

## How to run this software 
- Install python from website - https://www.python.org/downloads/
- Install python packages
```csv
pip install pyqt6 pyqtgraph pyserial

- Run using command
```csv
python <name-of-your-file>.py

-if you want to run through command prompt in windows just navigate to your folder in command prompt and write above command.
```csv
pyhton <name-of-your-file>.py

Thank you!