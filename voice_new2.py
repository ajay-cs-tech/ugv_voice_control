import whisper
import pyaudio
import wave
import time
import requests
import os
import numpy as np
import soundfile as sf

# IP of the Arduino
ARDUINO_IP = "http://192.168.4.1"

# Whisper model
print("🔁 Loading Whisper model...")
model = whisper.load_model("base")

# Audio config
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "temp.wav"

# Command variations (fuzzy match)
COMMANDS = {
    "forward": ["forward", "for work", "for word", "fordward", "foward"],
    "backward": ["back", "backward", "go back", "reverse"],
    "left": ["left", "turn left"],
    "right": ["right", "turn right"],
    "stop": ["stop", "halt", "pause"]
}

def match_command(text):
    for cmd, variants in COMMANDS.items():
        if any(word in text for word in variants):
            return cmd
    return None

def send_command_to_arduino(command):
    try:
        requests.get(f"{ARDUINO_IP}/{command}", timeout=2)
        print(f"✅ Sent: {command.upper()}")
    except requests.exceptions.RequestException as e:
        print(f"🚫 Network error: {e}")

def listen_once():
    print("🎤 Listening for command...")
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Convert and normalize
    audio = np.frombuffer(b''.join(frames), dtype=np.int16).astype(np.float32) / 32768.0
    audio *= 2.0  # Volume boost
    sf.write(WAVE_OUTPUT_FILENAME, audio, RATE)

    return WAVE_OUTPUT_FILENAME

def main():
    print("✅ Say: forward, back, left, right, stop")
    print("🌐 Ensure you're connected to the Arduino's Wi-Fi\n")

    while True:
        try:
            audio_file = listen_once()
            result = model.transcribe(audio_file, language='en')
            text = result["text"].strip().lower()
            print(f"🗣️ Heard: {text}")

            command = match_command(text)
            if command:
                send_command_to_arduino(command)
            else:
                print("⚠️ Unknown command")

            time.sleep(0.5)  # Small delay to avoid overwhelming loop
        except KeyboardInterrupt:
            print("👋 Exiting...")
            break
        except Exception as e:
            print(f"🔥 Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
