import threading
import socket
from os import _exit
from termcolor import colored

class Users:
    """
    For define all users including the server
    """
    c_list = []

    def __init__(self, addr:str, port:int, username:str, client):
        """
        Defining all specs and append c_list as a dict if its not server
        """
        self.addr = addr
        self.port = port
        self.username = username
        self.client = client
        self.__dict__ = {
            'addr': addr,
            'port': port,
            'username': username,
            'client': client
        }
        if (self.username != "Server"):
            self.c_list.append(self.__dict__)
    
    def listen_client(self):
        """
        This function listens for clients to receive messages. If the message is not empty, 
        it sends a message to all users with the boradcast_mesage function. This function 
        should run with thread
        """
        while 1:
            try:
                message = self.client.recv(2048).decode('utf-8').strip()

                if len(message) > 0:

                    broadcast_message(self, message)
            except ConnectionResetError:
                print(colored(f"{self.username} has been disconnected!", 'red'))
                self.c_list.remove(self.__dict__)
                break
            except Exception as err:
                print("error", err)
                break

def register_users(server):
    """
    This function is waiting for new clients. New clients must choose a username to send messages. 
    The function checks if the username is available. If the username is available, 
    it registers as a user in the Users class. This function should run with thread
    """
    while 1:
        c, addr = server.accept()

        try:
            username = c.recv(1024).decode('utf-8').strip()
            is_available = is_username_available(username)
            while(not is_available[0]):
                c.send(colored(is_available[1], "red").encode('utf-8'))
                c.send(colored('\nPleas enter a new username', "green").encode('utf-8'))

                username = c.recv(1024).decode('utf-8').strip()

                is_available = is_username_available(username)

        except ConnectionResetError:
            continue

        user = Users(addr[0], addr[1], username, c)
        threading.Thread(target=user.listen_client).start()
        print(f"{addr}, connected as {username}")

def broadcast_message(client, message:str):
    """
    This function sending message to all users.
    """
    print(f"{colored(client.username, 'white', attrs=['bold'])}: {message}")
    for target in Users.c_list:
        if target['client'] == client.client:
            target['client'].send(f"{colored('You', 'white', attrs=['bold'])}: {message}".encode('utf-8'))
        else:
            target['client'].send(f"{colored(client.username, 'white', attrs=['bold'])}: {message}".encode('utf-8'))

def commands(input_value:str, server_u):
    """
    This function runing commands or sending message from server
    """
    if input_value.startswith('!'):
        if input_value =='!exit':
            _exit(1)
    else:
        broadcast_message(server_u, input_value) 
     

def wait_for_command(server):
    """
    This function wait for command from server. This function should run with thread.
    """
    while 1:
        command = input("").strip()

        if command:
            commands(command, server)
       
def is_username_available(username):
    """
    This funciton checks a username is it available.
    """
    if username == "Server":
        return (False, "You cant take this username")
    
    username_list = [name['username']==username for name in Users.c_list]

    return (not any(username_list), "This username is taken")
