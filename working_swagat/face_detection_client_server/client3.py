
import socket, cv2, pickle, struct, imutils
# create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = ''  # paste your server ip address here
port = 5001
client_socket.connect((host_ip, port))  # a tuple
data = b""

vid = cv2.VideoCapture(0)

while (vid.isOpened()):
    img, frame = vid.read()
    frame = imutils.resize(frame, width=320)
    a = pickle.dumps(frame)
    message = struct.pack("Q", len(a)) + a
    client_socket.sendall(message)

    cv2.imshow('TRANSMITTING VIDEO', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        client_socket.close()