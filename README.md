# Minecraft Server Manager
Automatically start, stop and remotely manage your Minecraft Server. This program consists of a Server Manager script (ServerMan.py) and a client (client.py) which you can make a wrapper around. The server manager will turn off the server if no one is there for a certain amount of time. The client will get the status of the server or request to turn on the server.

# How to Use
- Enable RCON on your minecraft server. Set the host (in ServerMan.py) to the IP adrress to the of the minecraft server. 
- The port in ServerMan.py is for the Server Manager to talk to the client. Set the host (in client.py) to the IP adrress of the device running ServerMan.py. The port in client.py should match the port in ServerMan.py.
- Enter the RCON password in pwd.txt in the same directory.
- Run ServerMan.py. You can make a wrapper around client.py and as soon as the script is run it will request the server to start or get the server staus.
