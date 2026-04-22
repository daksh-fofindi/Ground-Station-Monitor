import serial
import sys
import time
from collections import deque
from statistics import mean
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtCore import QTimer
import pyqtgraph as pg

# ================= SERIAL CONFIG =================
PORT = "COM4"      # 🔴 change to your ESP32 COM port
BAUD = 115200
ser = serial.Serial(PORT, BAUD, timeout=1)

# ================= TIME =================
start_time = time.time()

# ================= BUFFER SIZE =================
N = 250

alt = deque(maxlen=N)
temp = deque(maxlen=N)
press = deque(maxlen=N)
rssi_buf = deque(maxlen=N)

ax = deque(maxlen=N)
ay = deque(maxlen=N)
az = deque(maxlen=N)

gx = deque(maxlen=N)
gy = deque(maxlen=N)
gz = deque(maxlen=N)

for _ in range(N):
    alt.append(0); temp.append(0); press.append(0); rssi_buf.append(-120)
    ax.append(0); ay.append(0); az.append(0)
    gx.append(0); gy.append(0); gz.append(0)

# ================= APP =================
app = QApplication(sys.argv)
pg.setConfigOption("background", "#0b0f14")
pg.setConfigOption("foreground", "#cfd8dc")

window = QWidget()
window.setWindowTitle("S.P.H.E.R.E. Rocket Ground Station")
window.resize(1550, 920)

# ================= GLASS STYLE =================
window.setStyleSheet("""
QWidget {
    background-color: #0b0f14;
    color: #eaeff2;
    font-family: Segoe UI;
}
QFrame {
    background-color: rgba(20, 25, 32, 180);
    border: 1px solid rgba(255,255,255,40);
    border-radius: 12px;
}
QLabel { background: transparent; }
""")

# ================= PLOT FACTORY =================
def glass_plot(title):
    p = pg.PlotWidget(title=title)
    p.setBackground(None)
    p.showGrid(x=True, y=True, alpha=0.15)
    return p

# ================= PLOTS =================
alt_plot = glass_plot("Altitude (m)")
temp_plot = glass_plot("Temperature (°C)")
press_plot = glass_plot("Pressure (hPa)")
rssi_plot = glass_plot("Signal Strength RSSI (dBm)")
acc_plot = glass_plot("Acceleration (m/s²)")
gyro_plot = glass_plot("Gyroscope (deg/s)")

alt_line = alt_plot.plot(alt, pen=pg.mkPen("#ffd54f", width=2))
temp_line = temp_plot.plot(temp, pen=pg.mkPen("#ef5350", width=2))
press_line = press_plot.plot(press, pen=pg.mkPen("#4dd0e1", width=2))
rssi_line = rssi_plot.plot(rssi_buf, pen=pg.mkPen("#ce93d8", width=2))

ax_l = acc_plot.plot(ax, pen=pg.mkPen("#ff5252"))
ay_l = acc_plot.plot(ay, pen=pg.mkPen("#69f0ae"))
az_l = acc_plot.plot(az, pen=pg.mkPen("#448aff"))

gx_l = gyro_plot.plot(gx, pen=pg.mkPen("#ff5252"))
gy_l = gyro_plot.plot(gy, pen=pg.mkPen("#69f0ae"))
gz_l = gyro_plot.plot(gz, pen=pg.mkPen("#448aff"))

# ================= AVERAGE LINES =================
alt_avg = pg.InfiniteLine(angle=0, pen=pg.mkPen("#ffd54f", style=pg.QtCore.Qt.PenStyle.DashLine))
temp_avg = pg.InfiniteLine(angle=0, pen=pg.mkPen("#ef5350", style=pg.QtCore.Qt.PenStyle.DashLine))
press_avg = pg.InfiniteLine(angle=0, pen=pg.mkPen("#4dd0e1", style=pg.QtCore.Qt.PenStyle.DashLine))
rssi_avg = pg.InfiniteLine(angle=0, pen=pg.mkPen("#ce93d8", style=pg.QtCore.Qt.PenStyle.DashLine))

alt_plot.addItem(alt_avg)
temp_plot.addItem(temp_avg)
press_plot.addItem(press_avg)
rssi_plot.addItem(rssi_avg)

# ================= INFO PANEL =================
info_panel = QFrame()
info_layout = QVBoxLayout(info_panel)

link = QLabel("🟢 RF LINK ACTIVE")
link.setStyleSheet("font-size:20px; color:#69f0ae")

values = QLabel("Waiting for telemetry...")
values.setStyleSheet("font-size:16px")

info_layout.addWidget(link)
info_layout.addWidget(values)
info_layout.addStretch()

# ================= LAYOUT =================
left = QVBoxLayout()
for w in [alt_plot, temp_plot, press_plot, rssi_plot, acc_plot, gyro_plot]:
    left.addWidget(w)

main = QHBoxLayout()
main.addLayout(left, 4)
main.addWidget(info_panel, 2)
window.setLayout(main)

# ================= UPDATE LOOP =================
def update():
    try:
        line = ser.readline().decode(errors="ignore").strip()
        if not line:
            return

        parts = line.split(",")

        # Ignore junk lines like single numbers
        if len(parts) < 15:
            return

        (
            pkt, dt, size,
            t, p, a,
            ax_v, ay_v, az_v,
            gx_v, gy_v, gz_v,
            rssi, snr, freqErr
        ) = map(float, parts[:15])

        # Fake MOSFET states (demo safe)
        mosfet1 = False
        mosfet2 = False

        mission_time = time.time() - start_time

        # Update buffers
        alt.append(a); temp.append(t); press.append(p); rssi_buf.append(rssi)
        ax.append(ax_v); ay.append(ay_v); az.append(az_v)
        gx.append(gx_v); gy.append(gy_v); gz.append(gz_v)

        # Update plots
        alt_line.setData(alt)
        temp_line.setData(temp)
        press_line.setData(press)
        rssi_line.setData(rssi_buf)

        ax_l.setData(ax); ay_l.setData(ay); az_l.setData(az)
        gx_l.setData(gx); gy_l.setData(gy); gz_l.setData(gz)

        # Update averages
        alt_avg.setValue(mean(alt))
        temp_avg.setValue(mean(temp))
        press_avg.setValue(mean(press))
        rssi_avg.setValue(mean(rssi_buf))

        # Update info panel
        values.setText(
            f"MISSION TIME: {mission_time:.1f} s\n\n"
            f"PACKET #: {int(pkt)}\n"
            f"INTERVAL: {int(dt)} ms\n"
            f"PACKET SIZE: {int(size)} bytes\n\n"
            f"MOSFET 1: FALSE\n"
            f"MOSFET 2: FALSE\n\n"
            f"ALTITUDE: {a:.1f} m\n"
            f"TEMP: {t:.1f} °C\n"
            f"PRESSURE: {p:.1f} hPa\n\n"
            f"ACCEL (X,Y,Z): {ax_v:.2f}, {ay_v:.2f}, {az_v:.2f}\n"
            f"GYRO (X,Y,Z): {gx_v:.2f}, {gy_v:.2f}, {gz_v:.2f}\n\n"
            f"RSSI: {rssi:.0f} dBm\n"
            f"SNR: {snr:.1f} dB\n"
            f"FREQ ERROR: {freqErr:.0f} Hz"
        )

        link.setText("🟢 RF LINK ACTIVE")

    except:
        link.setText("🔴 TELEMETRY ERROR")
        link.setStyleSheet("color:#ff5252")

# ================= TIMER =================
timer = QTimer()
timer.timeout.connect(update)
timer.start(50)

window.show()
sys.exit(app.exec())
