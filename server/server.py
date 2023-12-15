import socket
import threading
from time import sleep
from os import _exit
from termcolor import colored
from func import *

host = "127.0.0.1"# Replace here
port = 1604

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server_u = Users(host, port, "Server", server)
 
try:
    server.listen(5)


    threading.Thread(target=lambda: register_users(server)).start()
    threading.Thread(target=lambda: wait_for_command(server_u)).start()

except socket.error as err:
    print("Error:", err)
except KeyboardInterrupt:
    _exit(1)