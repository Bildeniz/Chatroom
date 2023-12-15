import socket
import threading
from os import _exit
from termcolor import colored

s = socket.socket()

host="127.0.0.1"# Replace here
port=1604

def listen_messages(socket:socket.socket):
    """
    This function for listening messages from server. Its should running with thread.
    """
    try:
        while 1:
            print(socket.recv(1024).decode('utf-8'))

    except ConnectionResetError:# If any problem exist with connection
        print(colored("Connection lost!", "red")) # Print this message
        _exit(1)

try:
    s.connect((host, port))#Connect Server

    print(colored("Connection successful!", "green"))

    username = input("Pleas enter a nickname: ")
    s.send(username.encode("utf-8"))# Send username to server

    threading.Thread(target=lambda: listen_messages(s)).start()# Start thread for listen message

    while 1:# Send every input to server 
        data = input().strip()
        if len(data)>0:
            s.send(data.encode('utf-8'))


except ConnectionResetError:# If server connection is have a problem
    print(colored("Connection lost!", "red"))
    _exit(1)
except ConnectionRefusedError:# If the server is not found
    print(colored("Could not find the Server", "red"))
    _exit(1)
except KeyboardInterrupt:# If user press ctrl+c
    _exit(1)
except socket.error as err:
    print(colored("Error!", "red"), colored(err, 'magenta'))
