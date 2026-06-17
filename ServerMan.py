import socket
import codes
from mcstatus import JavaServer
import mcrcon
import subprocess
import select

HOST = "127.0.0.1"
PORT = 25545
SERVER_PORT = 25565

SERVER_STOP_TIMEOUT = 300

SERVER_MEM_ALLOCATION = "4G"

with open("pwd.txt","r") as f:
    RCON_PWD = f.read()

Server_Status = False

SERVER_PATH = "D:/server/server.jar"
SERVER_DIRECTORY = "D:/server"
serverStatusSocket = JavaServer(HOST, SERVER_PORT)

def checkServerStatus():
    global Server_Status
    # if the server is online this code does not throw an exception
    prevState = Server_Status
    try:
        status = serverStatusSocket.status()
        Server_Status = True
    except:
        Server_Status = False
    
    if prevState and not Server_Status:
        print("Server shutdown detected.")
        pass

def startServer(conn):
    checkServerStatus()

    if Server_Status:
        conn.sendall(codes.SERVER_RUNNING)
        return

    print("Starting server")
    subprocess.Popen(
        f"java -jar -Xmx{SERVER_MEM_ALLOCATION} -Xms{SERVER_MEM_ALLOCATION} {SERVER_PATH}",
        cwd = SERVER_DIRECTORY,
        stdout= subprocess.DEVNULL,
        stderr= subprocess.DEVNULL
    )
    conn.sendall(codes.SERVER_STARTING)

def getPlayerCount():
    checkServerStatus()

    if not Server_Status:
        return
    
    status = serverStatusSocket.status()
    return status.players.online

def stopServer():
    if getPlayerCount() != 0:
        #print("Server in use. Not stopping Server")
        return
    
    server = mcrcon.MCRcon(HOST, RCON_PWD)
    try:
        server.connect()
        
        server.command("stop")
        print("Server Stoped")

        server.disconnect()
    
    except:
        print("Server Shutdown unsuccesful")
        pass

    checkServerStatus()

print("Server Manager Started")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as qSock:
    qSock.bind(("0.0.0.0",PORT))
    qSock.listen()

    while True:
        readable, _, _ = select.select([qSock], [], [], SERVER_STOP_TIMEOUT)

        if not readable:
            stopServer()
            continue

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

