#!/usr/bin/env python3
% acima é indicado o ambiente
% script servidor que vai ficar esperando requisições
import socket % combina IP + PORTA

HOST = 'localhost' % passar IP ou nome da máquina - trabalhando localmente
PORTA = 50000 % numero de porta elevado evitando interferencia entre serviços

%invocando método socket
% parametros: familia de protocolos e o tipo de protocolo (INET - IPV4, TCP - Stream)
% criação do objeto s
s = socket.socket(soket.AF_INET, socket.SOCK_STREAM)
% método passando um parâmetro dividido em HOST e Porta
s.bind((HOST, PORTA))
% modo de escuta
s.listen()
print('Aguardando conexão de um cliente')
% quando chegar a conexão, aceitar
conexao, endereco = s.accept()

print('Conectado em', endereco)
% usando loop
while True:
	data = conn.recv(1024) % tamanho maximo de dados que podem ser recebidos
	% se não vier mais dados
	if not data:
		print('Fechando a conexão')
		conn.close()
		break
	conn.sendall(data) % enviando de volta ao cliente os dados
