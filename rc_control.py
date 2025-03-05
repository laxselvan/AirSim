import airsim
import pygame
import time

# Initialize AirSim Client
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# Initialize Joystick
pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

# Controller Axis Mapping for TX16S (Swapped Yaw & Throttle)
ROLL_AXIS = 0       # Right stick (Left/Right) - Moves drone left/right
PITCH_AXIS = 1      # Right stick (Up/Down) - Moves drone forward/backward
YAW_AXIS = 3        # Left stick (Up/Down) - Rotates drone (Now Continuous)
THROTTLE_AXIS = 2   # Left stick (Left/Right) - Moves drone up/down

# Scaling & Deadzone
DEADZONE = 0.05
SMOOTHING_FACTOR = 0.1  # Adjust for smoother response
ALTITUDE_SCALE = 3    # Adjust altitude control speed
YAW_SCALE = 1.0         # Adjust yaw rotation speed (Increased for continuous rotation)

def apply_deadzone(value):
    """Apply deadzone filtering."""
    return 0 if abs(value) < DEADZONE else value

# Initialize movement variables
roll, pitch, yaw, altitude = 0, 0, 0, 0

while True:
    pygame.event.pump()  # Update joystick events

    # Read inputs with smoothing
    roll = (1 - SMOOTHING_FACTOR) * roll + SMOOTHING_FACTOR * apply_deadzone(joystick.get_axis(ROLL_AXIS))
    pitch = (1 - SMOOTHING_FACTOR) * pitch + SMOOTHING_FACTOR * apply_deadzone(joystick.get_axis(PITCH_AXIS))
    yaw_input = apply_deadzone(joystick.get_axis(YAW_AXIS))  # Now controls rotation
    throttle_input = apply_deadzone(joystick.get_axis(THROTTLE_AXIS))  # Now controls altitude

    # Convert throttle input to altitude control (Now moved to Left Stick Left/Right)
    current_altitude = client.getMultirotorState().kinematics_estimated.position.z_val
    new_altitude = current_altitude - (throttle_input * ALTITUDE_SCALE)  

    # Ensure yaw rotation is continuous (Instead of snapping back)
    yaw += yaw_input * YAW_SCALE  # Accumulate yaw rotation

    # Send movement command
    client.moveByRollPitchYawZAsync(roll, pitch, yaw, new_altitude, 0.05)

    # Debugging: Print values
    print(f"Roll: {roll:.2f}, Pitch: {pitch:.2f}, Yaw: {yaw:.2f}, Throttle Input: {throttle_input:.2f} -> Altitude: {new_altitude:.2f}")

    time.sleep(0.05)  # Small delay for stability
