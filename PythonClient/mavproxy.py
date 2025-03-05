import airsim
import sys
import time
from pymavlink import mavutil

def run_mavlink_proxy():
    # Connect to AirSim
    client = airsim.MultirotorClient()
    client.confirmConnection()

    # Create a MAVLink connection
    master = mavutil.mavlink_connection('udpout:127.0.0.1:14551')

    while True:
        # Get drone state from AirSim
        state = client.getMultirotorState()

        # Create a MAVLink message (example: heartbeat)
        msg = master.mav.heartbeat_encode(
            mavutil.mavlink.MAV_TYPE_QUADROTOR,
            mavutil.mavlink.MAV_AUTOPILOT_GENERIC,
            0, 0, 0
        )

        # Send the MAVLink message
        master.mav.send(msg)

        # Sleep for a short time
        time.sleep(0.1)

if __name__ == "__main__":
    run_mavlink_proxy()