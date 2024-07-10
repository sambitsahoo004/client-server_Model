# server.py

import socket
from random import *

HEADER = 256
FORMAT = 'utf-8'
PORT = 8081
SERVERIP = "127.0.0.1"
ADDR = (SERVERIP, PORT)

prisoner_escape = []
temp_list = []
L = randint(1, 400)
R = randint(L + 10000, L + 100000)
X = randint(L, R)
prisoner_list = []
shared_pool = []

def receive(client):
    try:
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)
        return msg
    except:
        return ""

def send(client, msg):
    message = str(msg).encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def client_communication(prisoner_list, shared_pool):
    global prisoner_escape
    global temp_list

    while True:
        if temp_list != prisoner_escape:
            for j in prisoner_escape:
                if j not in temp_list:
                    for i in range(len(prisoner_list)):
                        if (i + 1) not in prisoner_escape:
                            client_socket = prisoner_list[i]
                            send(client_socket, "\n[SERVER]!!!!  PRISONER " + str(j) + " HAS ESCAPED  !!!!\n")
                    temp_list.append(j)
        for i in range(len(prisoner_list)):
            if (i + 1) not in prisoner_escape:
                client_socket = prisoner_list[i]
                send(client_socket, "no more escaped prisoners")

        pool_guesses = []

        for i in range(len(prisoner_list)):
            if (i + 1) not in prisoner_escape:
                client_socket = prisoner_list[i]

                send(client_socket, "Start")
                guess = int(receive(client_socket))

                if i + 1 in shared_pool:
                    pool_guesses.append(guess)

                if guess > X:
                    send(client_socket, '[SERVER] HIGH')
                elif guess < X:
                    send(client_socket, '[SERVER] LOW')
                elif guess == X:
                    send(client_socket, '[SERVER] CORRECT')
                    prisoner_escape.append(i + 1)

        for i in range(len(prisoner_list)):
            if (i + 1) not in prisoner_escape:
                client_socket = prisoner_list[i]
                if i + 1 in shared_pool:
                    send(client_socket, f"[SERVER] SHARED POOL GUESSES: {pool_guesses}")

        if len(prisoner_escape) == len(prisoner_list):
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(ADDR)
    server_socket.listen()

    print("Initial range is ", L, "to", R, "and the lucky number is=", X)
    print("Waiting for connection...")

    num_prisoners = int(input("Enter the number of prisoners: "))

    while len(prisoner_list) < num_prisoners:
        client_socket, client_address = server_socket.accept()
        prisoner_list.append(client_socket)
        print("New connection @ ", client_address)
        send(client_socket, "Welcome to the Server, successfully connected!")

        join_pool = receive(client_socket)
        if join_pool.lower() == 'yes':
            shared_pool.append(len(prisoner_list))

        send(client_socket, str(L))
        send(client_socket, str(R))

    client_communication(prisoner_list, shared_pool)

print("\nOrder of escape :")
for i in prisoner_escape:
    print("Prisoner number " + str(i))

