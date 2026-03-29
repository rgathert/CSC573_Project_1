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

    return server_socket


server_socket = serverSocket()


# Adding in server specific functions not in general function

