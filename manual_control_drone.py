import airsim
import time
import threading
from pynput import keyboard

# Connect to AirSim
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# Takeoff
client.takeoffAsync().join()

# Movement parameters
max_speed = 10.0  # Increased Max speed (m/s)
acceleration = 0.3  # Faster acceleration
deceleration = 0.3  # Smoother stopping
altitude_speed = 5.0  # Faster up/down speed
update_rate = 0.05  # Update interval (smooth control)

# Current velocity
vx, vy, vz = 0, 0, 0
keys_pressed = set()
running = True

def update_movement():
    """Gradually adjusts velocity for smoother & faster movement."""
    global vx, vy, vz

    while running:
        target_vx, target_vy, target_vz = 0, 0, 0

        # Determine target velocity
        if 'w' in keys_pressed:  # Forward
            target_vx = max_speed
        if 's' in keys_pressed:  # Backward
            target_vx = -max_speed
        if 'a' in keys_pressed:  # Left
            target_vy = -max_speed
        if 'd' in keys_pressed:  # Right
            target_vy = max_speed
        if 'q' in keys_pressed:  # Up
            target_vz = -altitude_speed
        if 'e' in keys_pressed:  # Down
            target_vz = altitude_speed

        # Apply gradual acceleration/deceleration
        vx += (target_vx - vx) * acceleration
        vy += (target_vy - vy) * acceleration
        vz += (target_vz - vz) * acceleration

        # Send movement command
        client.moveByVelocityAsync(vx, vy, vz, update_rate)

        time.sleep(update_rate)

# Keyboard event handlers
def on_press(key):
    try:
        key_char = key.char.lower()
        if key_char in ['w', 'a', 's', 'd', 'q', 'e']:
            keys_pressed.add(key_char)
    except AttributeError:
        pass

def on_release(key):
    global running
    try:
        key_char = key.char.lower()
        if key_char in keys_pressed:
            keys_pressed.remove(key_char)
    except AttributeError:
        if key == keyboard.Key.esc:
            print("Exiting control...")
            running = False
            client.landAsync().join()
            client.armDisarm(False)
            client.enableApiControl(False)
            return False  # Stop the listener

# Start movement update thread
movement_thread = threading.Thread(target=update_movement, daemon=True)
movement_thread.start()

# Start keyboard listener
print("Use W/A/S/D for movement, Q/E for up/down, ESC to exit.")
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
listener.join()
