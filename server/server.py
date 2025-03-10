import protocols_answer.game_protocol_op
import protocols_answer.login_protocol_op
import protocols_answer.cloud_protocol_op
from protocols_answer.sendingOperations import*
import socket
import select
from collections import deque
import time
import threading
import global_server_op

def main():
    """running the server."""
    global_server_op.init()
    print("server is up and running")

    while True:
        reading,writing,errors= select.select(list(global_server_op.sock_username.keys())+[global_server_op.server_socket],[],list(global_server_op.sock_username.keys()))
        for sock in errors:
            global_server_op.sock_username.pop(sock)

        for sock in reading:
            if sock==global_server_op.server_socket:
                (new_socket, address) = global_server_op.server_socket.accept()
                username= global_server_op.choose_unloged_username()
                global_server_op.OnConect(username,new_socket,address[0])
                print("username:",username)
                continue

            if not sock in global_server_op.sock_username.keys():
                continue

            msg= unpucketMasegTCP(sock)
            if msg!="":
                print(msg,global_server_op.sock_username[sock])
            categoryInd= msg.find("|")
            if categoryInd==-1:
                if msg=="GEXIT":
                    global_server_op.GExit(sock)
                elif msg=="!":
                    global_server_op.sock_connect_msg[sock]=True
                continue
            print(msg[:categoryInd])
            if msg[:categoryInd]=="GAME":
                protocols_answer.game_protocol_op.TCP_meseg_handle(msg[categoryInd+1:],global_server_op.sock_username[sock])
            elif msg[:categoryInd]=="LOGIN":
                protocols_answer.login_protocol_op.TCP_meseg_handle(msg[categoryInd+1:],sock)
            elif msg[:categoryInd]=="CLOUD":
                protocols_answer.cloud_protocol_op.TCP_meseg_handle(msg[categoryInd + 1:], global_server_op.sock_username[sock], sock)
            elif msg[:categoryInd]=="PUBLIC KEY":
                get_public_key(sock,msg[categoryInd + 1:])

if __name__=="__main__":
    main()
