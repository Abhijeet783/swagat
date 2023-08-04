#latest
#added gesture feature and testing 4-8-23
import cv2
import socket, struct

from functions import face_detection,gesture_initialization,gesture_main,video_frame_receive
flag = 0
flag2 = 0
count = 0
count2 = 0
flag3=0
detected=0

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = '10.212.11.20'
print('HOST IP:', host_ip)
port = 5001
socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(1)
print("LISTENING AT:", socket_address)
payload_size = struct.calcsize("Q")
data = b""

# gusture initialization

gesture_initialization()


while True:
    #global count2, flag, count, flag2, flag3,detected
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        while True:

            video_frame_receive()

            message = client_socket.recv(1024).decode()
            print('received msg:', message)
            if message=='audio_finished':
                gesture_main()
            else:
                face_detection()

#............................................
            cv2.imshow("RECEIVING VIDEO", img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
