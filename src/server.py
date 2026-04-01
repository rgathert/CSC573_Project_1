import socket
import os
import sys
import multiprocessing as mp

host_names = {}
port_number = {}
# Server Socket to Listen to Clients
def serverSocket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost',7734)) #TODO: Get a proper IP
    server_socket.listen(5)
    return server_socket

def clientHandling(server_connection):
    print("Peer_Conn_test")
    data = server_connection.recv(1024).decode()

    (client_part, rfc_part) = data.split(',')

    client_name = client_part.split(': ')[1]
    rfc_id = rfc_part.split(': ')[1].split()

    print(f'Client Hostname: {client_name}')
    print(f'Mai RFC: = {rfc_id}')
    server_connection.close()
    print("Connection done test")
if __name__ == '__main__':
    server_socket = serverSocket()


    # Adding in server specific functions not in general function
    # TODO: Make these functions work to be server specific

    while True:
        (server_connection, server_address) = server_socket.accept()
        server_process = mp.Process(target = clientHandling, args=(server_connection,))
        server_process.daemon = True
        server_process.start()