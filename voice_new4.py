import whisper
import sounddevice as sd
import numpy as np
import queue
import requests
import re
import time

# === CONFIGURATION ===
ARDUINO_IP = "http://192.168.4.1"
SAMPLE_RATE = 16000
BLOCK_DURATION = 3  # seconds
COMMAND_TIMEOUT = 2

# === LOAD WHISPER MODEL ===
print("🔁 Loading Whisper model...")
model = whisper.load_model("base")

# === AUDIO QUEUE ===
audio_queue = queue.Queue()

# === NATURAL LANGUAGE COMMANDS ===
COMMAND_MAP = {
    "forward": r"\b(forward|go forward|move ahead|go ahead|move forward|start moving)\b",
    "backward": r"\b(back|go back|reverse|move back|backward)\b",
    "left": r"\b(left|turn left|veer left|go left)\b",
    "right": r"\b(right|turn right|veer right|go right)\b",
    "stop": r"\b(stop|halt|pause|hold on|freeze)\b"
}

def match_command(text):
    for command, pattern in COMMAND_MAP.items():
        if re.search(pattern, text):
            return command
    return None

def send_command(command):
    try:
        requests.get(f"{ARDUINO_IP}/{command}", timeout=COMMAND_TIMEOUT)
        print(f" Sent: {command.upper()}")
    except requests.exceptions.RequestException as e:
        print(f" Network error: {e}")

def audio_callback(indata, frames, time_info, status):
    if status:
        print("️ Mic warning:", status)
    audio_queue.put(indata.copy())

def main():
    print("Say commands like: 'go forward', 'please stop', 'turn left', etc.")
    print(" Ensure you're connected to Arduino Wi-Fi (192.168.4.1)")
    print(" Listening continuously... Press Ctrl+C to exit.\n")

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='float32', callback=audio_callback):
        buffer = np.empty((0,), dtype=np.float32)

        while True:
            try:
                block = audio_queue.get()
                buffer = np.concatenate((buffer, block.flatten()))

                # Process every BLOCK_DURATION seconds
                if len(buffer) >= SAMPLE_RATE * BLOCK_DURATION:
                    audio_block = buffer[:SAMPLE_RATE * BLOCK_DURATION]
                    buffer = buffer[SAMPLE_RATE * BLOCK_DURATION:]  # keep leftover

                    result = model.transcribe(audio_block, language="en", fp16=False)
                    text = result["text"].strip().lower()

                    if text:
                        print(f"️ Heard: {text}")
                        command = match_command(text)
                        if command:
                            send_command(command)
                        else:
                            print(" Didn't understand command.")
                    else:
                        print(" Silence or unclear speech.")

            except KeyboardInterrupt:
                print("Exiting...")
                break
            except Exception as e:
                print(f" Error: {e}")
                time.sleep(1)

if __name__ == "__main__":
    main()

