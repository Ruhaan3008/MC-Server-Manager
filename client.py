import socket
import codes

HOST = "127.0.0.1"
PORT = 25545
def client_request():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSock:
        try:
            serverSock.connect((HOST, PORT))
        except:
            print("Error connecting with the server")
            return
            
        print("Connection established")
        
        try:
            serverSock.sendall(codes.SERVER_START_REQUEST)
            data = serverSock.recv(1024)
            while True:
                data = serverSock.recv(1024)

                if not data:
                    break
            
                print(data.decode())

                if (data == codes.SERVER_STARTING) or (data == codes.SERVER_RUNNING):
                    break

                elif data == codes.SERVER_ERROR:
                    print("Server Error! Server not running")
                    break
                else:
                    serverSock.send(codes.IDLE)
        except:
            print("There was an error communicating")

if (__name__ == "__main__"):
    client_request()