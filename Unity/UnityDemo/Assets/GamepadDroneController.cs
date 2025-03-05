using UnityEngine;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

public class GamepadDroneController : MonoBehaviour
{
    private UdpClient client;
    private const int port = 5005;
    private bool isFlying = false;

    void Start()
    {
        client = new UdpClient();
        Debug.Log("Gamepad Drone Controller Initialized");
    }

    void Update()
    {
        float roll = Input.GetAxis("Horizontal");  // TX16s right stick X-axis
        float pitch = Input.GetAxis("Vertical");   // TX16s right stick Y-axis
        float yaw = Input.GetAxis("Joystick Axis 3"); // TX16s left stick X-axis
        float throttle = -Input.GetAxis("Joystick Axis 2"); // TX16s left stick Y-axis (inverted)

        // Normalize throttle (convert from [-1,1] to [0,1])
        throttle = (throttle + 1) / 2;

        // Send movement command to AirSim
        SendDroneCommand($"MOVE {roll},{pitch},{yaw},{throttle}");

        // Takeoff and Land using buttons
        if (Input.GetButtonDown("Joystick Axis 3") && !isFlying) // Button A
        {
            Debug.Log("Taking off...");
            SendDroneCommand("TAKEOFF");
            isFlying = true;
        }

        if (Input.GetButtonDown("Joystick Axis 2") && isFlying) // Button B
        {
            Debug.Log("Landing...");
            SendDroneCommand("LAND");
            isFlying = false;
        }
        Debug.Log("Joystick Axis 3 (Yaw): " + Input.GetAxis("Joystick Axis 3"));
        Debug.Log("Joystick Axis 2 (Throttle): " + Input.GetAxis("Joystick Axis 2"));

    }

    void SendDroneCommand(string command)
    {
        byte[] data = Encoding.ASCII.GetBytes(command);
        client.Send(data, data.Length, "127.0.0.1", port);
    }
}
