#!/usr/bin/env python3
% modulo socket
%
import socket

HOST = '127.0.0.1'
PORTA = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORTA))
s.sendall(str.encode('Bom dia servidor!'))
data = s.recv(1024) % receber um tamanho especifico maximo

print('Mensagem recebida pelo servidor:', data.decode())