import socket
import cv2
import base64

# Server configuration
host = '10.212.8.82'
port = 5001

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((host, port))
print('Connected to server:', host, port)

# Capture video frames
camera = cv2.VideoCapture(0)  # Change the camera index if needed

while True:
    # Capture frame from the camera
    ret, frame = camera.read()
    cv2.imshow('person',frame)
    cv2.waitkey(0)
    # Convert frame to JPEG
    _, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')

    # Send the frame to the server
    client_socket.send(jpg_as_text.encode())

    # Receive response from the server
    response = client_socket.recv(4096)
    if not response:
        break
    else:
        print('recieved')
    # Process the response (print detected faces in this example)
    print('Detected faces:', response.decode())

# Close the connection
client_socket.close()
