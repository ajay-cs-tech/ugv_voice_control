# 🔊 Voice-Controlled UGV over Wi-Fi (Arduino + Python + Whisper)

Control your Arduino-powered UGV robot with natural voice commands like:

> **"forward", "left", "stop"**

### 📦 Features
- 🎤 Real-time speech recognition using OpenAI's Whisper
- 📡 Sends commands over Wi-Fi via HTTP to Arduino
- 💻 Runs fully offline on your laptop using microphone
- 🔁 Always listening + fuzzy command matching

---

## 🚀 Setup

### 1. 🔧 Arduino Requirements
- Arduino Uno R4 WiFi (or ESP32)
- Motor driver (L298N)
- Expose HTTP endpoints:
  - `/forward`
  - `/backward`
  - `/left`
  - `/right`
  - `/stop`

### 2. 💻 Laptop Requirements

Install Python packages:

```bash
pip install -r requirements.txt

---
```
## 🔧 Arduino Setup

### 🛠️ Hardware
- Arduino Uno R4 WiFi
- Motor Driver (L298N)
- Tank chassis + motors
- 7.4V or 12V battery + switch

### 🔌 Wiring

| Motor Driver | Arduino Pin |
|--------------|-------------|
| ENA          | 9 (PWM)     |
| IN1          | 2           |
| IN2          | 4           |
| IN3          | 7           |
| IN4          | 8           |
| ENB          | 10 (PWM)    |

### 📡 Upload the Code

Upload `voice_wifi.ino` using Arduino IDE.

Your UGV will create a Wi-Fi hotspot named **UGV_ROBOT**.  
Connect your laptop to that before running the Python script.
