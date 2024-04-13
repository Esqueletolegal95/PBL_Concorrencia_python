import socket
import threading
from queue import Queue


HOST = '127.0.0.1'  # Endereço IP local
PORT = 65432        # Porta para escutar

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(HOST, PORT)
        s.listen()
        client_socket, addr = s.accept()
        
