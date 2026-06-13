import socket
import codes
from mcstatus import JavaServer
import mcrcon
import subprocess
import select

HOST = "127.0.0.1"
PORT = 25545

with open("pwd.txt","r") as f:
    RCON_PWD = f.read()

Server_Status = False

SERVER_PATH = "D:/server/server.jar"
SERVER_DIRECTORY = "D:/server"
serverStatusSocket = JavaServer("127.0.0.1", 25565)

def checkServerStatus():
    global Server_Status
    try:
        status = serverStatusSocket.status()
        Server_Status = True
    except:
        Server_Status = False

def startServer(conn):
    checkServerStatus()

    if Server_Status:
        conn.sendall(codes.SERVER_RUNNING)
        return

    print("Starting server")
    subprocess.Popen(
        f"java -jar -Xmx4G -Xms4G {SERVER_PATH}",
        cwd = SERVER_DIRECTORY,
        stdout= subprocess.DEVNULL,
        stderr= subprocess.DEVNULL
    )
    conn.sendall(codes.SERVER_STARTING)

def getPlayerCount():
    checkServerStatus()

    if not Server_Status:
        return 0
    
    status = serverStatusSocket.status()
    return status.players.online

def stopServer():
    if getPlayerCount() != 0:
        print("Server in use. Not stopping Server")
        return
    
    server = mcrcon.MCRcon("127.0.0.1", RCON_PWD)
    try:
        server.connect()
        
        server.command("stop")
        print("Server Stoped")

        server.disconnect()
    
    except:
        pass

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as qSock:
    qSock.bind((HOST,PORT))
    qSock.listen()

    while True:
        readable, _, _ = select.select([qSock], [], [], 300)

        if not readable:
            stopServer()

        else:
            conn, addr = qSock.accept()

            with conn:
                print(f"Connected to {addr}")
                while True:
                    data = conn.recv(1024)

                    if not data:
                        break 

                    if (data == codes.SERVER_START_REQUEST):
                        print(data.decode())
                        conn.sendall(codes.INITIATING_SERVER)
                        startServer(conn)
                        break

                    elif (data == codes.IDLE):
                        pass

