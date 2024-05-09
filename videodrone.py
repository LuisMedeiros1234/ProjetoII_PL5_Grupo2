import cv2
import socket
import threading
import time

from djitellopy import Tello

tello = Tello()

tello.connect()

# Tello drone's IP and command port
tello_address = ('192.168.10.1', 8889)

# Create a UDP connection for sending commands
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 9000))  # Bind to any port on localhost

# Function to send commands to the drone
def send_command(command):
    sock.sendto(command.encode(), tello_address)
    print(f"Command sent: {command}")

# Function to receive command responses from the drone
def receive():
    while True:
        try:
            response, ip_address = sock.recvfrom(1024)
            print(f"Received response: {response.decode()}")
        except Exception as e:
            print(f"Error receiving: {str(e)}")
            break

# Start the command response receiver thread
receive_thread = threading.Thread(target=receive)
receive_thread.daemon = True
receive_thread.start()

# Send command to initiate SDK mode
send_command('command')

# Send command to start video stream
send_command('streamon')

# Capture the video stream
cap = cv2.VideoCapture('udp://@0.0.0.0:11111')

# Check if the video capture has started successfully
if not cap.isOpened():
    print("Failed to open video stream")
else:
    print("Video stream opened successfully")

    try:
        # Display the video stream
        while True:
            ret, frame = cap.read()
            if ret:
                cv2.imshow('Tello', frame)
                
                # Exit if 'q' key is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
    finally:
        # Clean up
        cap.release()
        cv2.destroyAllWindows()
        send_command('streamoff')  # Turn off the stream
        sock.close()  # Close the socket

print("Shutting down connection...")
