import airsim
import time

# Connect to AirSim
client = airsim.MultirotorClient()
client.confirmConnection()
print("Drone connected!")

# Enable API control and arm the drone
client.enableApiControl(True)
client.armDisarm(True)
print("Drone armed!")

# Takeoff
client.takeoffAsync().join()
print("Drone took off!")

# Move forward
client.moveToPositionAsync(5, 0, -5, 3).join()  # Move 5m forward at 3m/s

# Land
client.landAsync().join()
print("Drone landed!")

# Release control
client.armDisarm(False)
client.enableApiControl(False)
print("Control released!")
