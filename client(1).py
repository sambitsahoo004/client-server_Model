# client.py

import socket
from random import *

HEADER = 256
FORMAT = 'utf-8'
PORT = 8081
SERVERIP = "127.0.0.1"
ADDR = (SERVERIP, PORT)
timestep = 1

def receive(client):
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
    return msg

def send(client, msg):
    message = str(msg).encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect(ADDR)
    salu = receive(client)
    print(salu)

    join_pool = input("Do you want to join the shared pool? (yes/no): ")
    send(client, join_pool)

    flag = 0
    while True:
        try:
            L = int(receive(client))
            R = int(receive(client))
            print("Range received = [", L, ",", R, "]", sep="")
            break
        except:
            print("Range not received")

    while True:
        print("Timestep", timestep)
        timestep += 1
        while True:
            escaped_prisoner = receive(client)
            if escaped_prisoner == "no more escaped prisoners":
                break
            else:
                print(escaped_prisoner)
        
        msg = receive(client)
        if msg.startswith("[SERVER] SHARED POOL GUESSES:"):
            pool_guesses = eval(msg.split(": ")[1])
            print("Shared Pool Guesses:", pool_guesses)
            if pool_guesses:
                # Use the information from the pool to adjust the guessing range
                L = min(pool_guesses) if min(pool_guesses) > L else L
                R = max(pool_guesses) if max(pool_guesses) < R else R
        
        if msg == "Start":
            Y = randint(L, R)
            print("My guess is", Y)
            send(client, str(Y))
            response = receive(client)
            print(response, "\n")
            if response == '[SERVER] HIGH':
                R = Y - 1
            elif response == '[SERVER] LOW':
                L = Y + 1
            elif response == '[SERVER] CORRECT':
                flag = 1

        if flag:
            print("You have escaped. Terminating program...")
            break

