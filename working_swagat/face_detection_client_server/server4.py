import socket, cv2, pickle, struct
import threading
flag = 0
flag2 = 0
count = 0
count2 = 0
flag3=0
detected=0
# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = '10.212.11.24'
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
# Socket Accept

def handle_client(client_socket):
    while True:
        # Receive and process messages from the client
        data = 'detected'
        server_socket.send(data.encode())  # send data to the client
        # Process the received message as needed
        print("message sent:", message)

while True:
    #global count2, flag, count, flag2, flag3,detected
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        while True:
            while len(data) < payload_size:

                packet = client_socket.recv(4 * 1024)  # 4K
                if not packet: break
                data += packet

            packed_msg_size = data[:payload_size]

            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4 * 1024)
            frame_data = data[:msg_size]

            data = data[msg_size:]

            img = pickle.loads(frame_data)

#.........................................
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            face_count = len(faces)
            if face_count != 0:
                print("face_detected")
                count += 1
                count2 = 0
                flag = 1

                if flag == 2:
                    count = 0
                    flag = 1
                if count > 10 and flag2 == 3:
                    print("***********playing sound . . . ")
                    #client_thread = threading.Thread(target=handle_client, args=(client_socket,))
                    #client_thread.start()
                    #client_thread.join()
                    response = "face detected "
                    client_socket.send(response.encode('utf-8'))
                    flag2 = 0
                    count = 0

            else:

                count2 += 1
                count = 0
                if count2 > 10:
                    flag2 = 3
                    count2 = 0
                print("face_not_detected")

                if flag == 1:
                    flag = 2

#............................................
            cv2.imshow("RECEIVING VIDEO", img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
