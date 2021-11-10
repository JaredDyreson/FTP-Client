"""
This file controls the ftp server
It receives commands from the client and sends/receives data to/from the client
"""


import os
import socket
import sys
import typing
import functools
import pathlib
from helpers import receive_all, send_all, send_err


class ftp_server:
    def __init__(self, server_port: int = 1233,
                 directory: pathlib.Path = pathlib.Path('/tmp/build')):
        if not(isinstance(server_port, int)
               and isinstance(directory, pathlib.Path)):
            #       and directory.is_dir()):
            raise ValueError(
                f'mismatched constructor: ftp_server({list(locals().values())[1:]})')
        self.server_port = server_port
        self.directory = directory
        self.welcome_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.welcome_sock.bind(('', self.server_port))

    def get(self, file_name: str, control: socket.socket) -> None:
        """requests a file from the server"""
        # tell the client that the command is OK
        send_all(control, 'OK')

        # TODO: create the data channel
        # TODO: send the data port number over control
        # TODO: wait for the client to connect
        # TODO: send the file over data
        # TODO: close data and the file

        print(f'get [{file_name}]')

    def put(self, file_name: str, control: socket.socket) -> None:
        """sends a file to the server"""
        # tell the client that the command is OK
        send_all(control, 'OK')

        # TODO: create the data channel
        # TODO: send the data port number over control
        # TODO: wait for the client to connect
        # TODO: receive the file over data
        # TODO: create and write the file
        # TODO: close data and the file

        print(f'put [{file_name}]')

    def ls(self, control: socket.socket) -> None:
        """lists the files located at the server"""
        # tell the client that the command is OK
        send_all(control, 'OK')

        # create the data channel and bind it to an available port
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.bind(('', 0))
        
        # listen
        data_socket.listen(1)

        # store the port num as str
        port_num = str(data_socket.getsockname()[1])

        # send the data port num to client over control
        send_all(control, port_num)

        # wait for client to connect over data
        data, addrs = data_socket.accept()

        # store shell command
        # file_list: str = os.popen("ls -l").read()
        file_list = 'this is the file list'

        # send the output over the 'data' channel
        send_all(data, file_list)

        # close the 'data' channel
        data.close()
        data_socket.close()

    def __del__(self):
        """clean up the object once we're done"""
        # close port
        self.welcome_sock.close()
        print(f"deleting object at {self}")

    def parse_args(self, socket: socket.socket, command: int) -> typing.Callable:
        def empty(): return None  # void function

        # get
        if command == 1:
            file_name = receive_all(socket)

            # TODO: check if file exists
            # This is an example fail case
            if file_name == 'getfail.txt':
                err_msg = f'{file_name} does not exist'
                send_err(socket, err_msg)
                print(err_msg)
                return empty

            return functools.partial(self.get, file_name, socket)

        # put
        if command == 2:
            file_name = receive_all(socket)

            # TODO: check if file exists
            # This is an example fail case
            if file_name == 'putfail.txt':
                err_msg = f'{file_name} already exists.'
                send_err(socket, err_msg)
                print(err_msg)
                return empty

            return functools.partial(self.put, file_name, socket)

        # ls
        if command == 3:
            return functools.partial(self.ls, socket)

        # quit
        if command == 4:
            socket.close()
            del self
        else:
            err_msg = 'Unknown command. Type \'help\' for the command list'
            send_err(socket, err_msg)
            return empty

    def loop(self):
        """receives and executes commands on loop"""
        self.welcome_sock.listen(1)

        print('Waiting for the client to connect...')
        control_sock, addr = self.welcome_sock.accept()

        print(f'Accepted connection from client {addr}')

        while True:
            print('Waiting for commands from client...')
            
            # command should be an integer.
            command_code = int(receive_all(control_sock))
            print(f'received command code {command_code}')

            # each command is parsed  into a function that is invoked here
            # it will break when it returns None
            try:
                self.parse_args(control_sock, command_code)()
            except TypeError:
                break

def main(argv: typing.List[str] = ["server.py", "1234"]):
    if not(argv):
        argv = sys.argv
    if len(argv) != 2:
        print(
            f'Usage: python {argv[0]} <Server Port>')

    server_port = argv[1]
    try:
        if((server_port := int(server_port)) < 0):
            print(
                f"[ERROR] Port number should not be negtive, received {server_port}")
            return
    except ValueError:
        print(
            f'[ERROR] Port should be number, received {server_port} of type {type(server_port)}')
        return

    server = ftp_server(server_port=server_port)
    server.loop()
    print('DONE')

if __name__ == '__main__':
    main()
    # to have it use sys.argv, call `main([])`