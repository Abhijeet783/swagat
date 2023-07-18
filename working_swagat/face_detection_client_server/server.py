import socket
import cv2
import numpy as np

# Server configuration
host = '10.212.11.20'#'localhost'
port = 5001#12345

# Load Haar cascade classifier for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(1)
print('Server listening on {}:{}'.format(host, port))

# Accept a client connection
client_socket, address = server_socket.accept()
print('Connected to client:', address)

while True:
    # Receive video frames from the client
    frame_data = client_socket.recv(4096)
    if not frame_data:
        break
    print('received')
    # Convert frame data to NumPy array
    frame_array = np.frombuffer(frame_data, dtype=np.uint8)

    # Decode the frame array
    frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
    cv2.imshow('img',frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    # Convert frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform face detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Prepare the response with detected faces
    response = {
        'faces': []
    }

    # Extract face coordinates and add to the response
    for (x, y, w, h) in faces:
        response['faces'].append({
            'x': int(x),
            'y': int(y),
            'width': int(w),
            'height': int(h)
        })

    # Send the response back to the client
    client_socket.send(str(response).encode())

# Close the connection
print('break!')
client_socket.close()
server_socket.close()
