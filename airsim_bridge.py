import airsim
import pygame

pygame.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

print("AirSim Joystick Control Active...")

try:
    while True:
        pygame.event.pump()

        # Get joystick values (adjust axis numbers based on test script output)
        roll = joystick.get_axis(0)        # Left/Right
        pitch = -joystick.get_axis(1)      # Forward/Backward (invert Y-axis)
        yaw = joystick.get_axis(2)         # Rudder/Rotation
        throttle = (joystick.get_axis(3) + 1) / 2  # Convert [-1,1] to [0,1]

        # Create RCData and send to AirSim
        rc_data = airsim.RCData()
        rc_data.roll = roll
        rc_data.pitch = pitch
        rc_data.yaw = yaw
        rc_data.throttle = throttle

        client.moveByRC(rc_data)

except KeyboardInterrupt:
    print("Stopping...")
    pygame.quit()
