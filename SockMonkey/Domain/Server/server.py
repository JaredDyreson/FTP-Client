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
import tempfile

from SockMonkey.Domain.Server.helpers import receive_all, send_all, send_err


class ftp_server:
    def __init__(self, server_port: int = 1233,
                 directory: pathlib.Path = pathlib.Path(f'{tempfile.gettempdir()}/build')):
        if not(isinstance(server_port, int)
               and isinstance(directory, pathlib.Path)):
            raise ValueError(
                f'mismatched constructor: ftp_server({list(locals().values())[1:]})')
        self.server_port = server_port
        self.directory = directory
        self.welcome_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.welcome_sock.bind(('', self.server_port))

        if not self.directory.is_dir():
            print(f'[INFO] Creating {self.directory}')
            print('[INFO] This is where the server\'s files are located')
            self.directory.mkdir()

    def get(self, file_name: str, control: socket.socket) -> None:
        """sends a file to the client"""
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
        print(f"[SERVER] Sending the port of {port_num}")
        send_all(control, port_num)

        # wait for client to connect over data
        data, addrs = data_socket.accept()

        # store shell command
        # our filesystem we have access to is /tmp/build , assuming linux
        print(f'[SERVER] Reading [{file_name}] from {self.directory}')
        with open(f'{self.directory}/{file_name}') as fp:
            content = ''.join(fp.readlines())
        # file_list = 'this is the file list'

        # send the output over the 'data' channel
        print('[SERVER] Sending...')
        send_all(data, content)

        print(f'[SERVER] [{file_name}] has been sent!')

        # close the 'data' channel
        data.close()
        data_socket.close()

    def put(self, file_name: str, control: socket.socket) -> None:
        """receives a file from the client"""
        # tell the client that the command is OK
        send_all(control, 'OK')
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.bind(('', 0))

        # listen
        data_socket.listen(1)

        # store the port num as str
        port_num = str(data_socket.getsockname()[1])

        # send the data port num to client over control
        print(f"[SERVER] Sending the port of {port_num}")
        send_all(control, port_num)

        data, addrs = data_socket.accept()

        print("[SERVER] Writing...")
        with open(f'{self.directory}/{file_name}', "w") as fp:
            fp.write(receive_all(data))

        print(f"[SERVER] [{file_name}] has been written to {self.directory}")

        data.close()
        data_socket.close()

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
        print(f"[SERVER] Sending the port of {port_num}")
        send_all(control, port_num)

        # wait for client to connect over data
        data, addrs = data_socket.accept()

        # store shell command
        # our filesystem we have access to is /tmp/build , assuming linux
        print(f'[SERVER] Getting the file list from {self.directory}')
        file_list: str = os.popen(f"ls -l {self.directory}").read()
        # file_list = 'this is the file list'

        # send the output over the 'data' channel
        print(f"[SERVER] Sending...")
        send_all(data, file_list)
        send_all(data, f'{self.directory}')

        print('[SERVER] File list has been sent!')

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

            if not pathlib.Path(f'{self.directory}/{file_name}').is_file():
                err_msg = (
                    f'{file_name} does not exist. Path = {self.directory}'
                )
                send_err(socket, err_msg)
                print(err_msg)
                return empty
            
            print(file_name, socket)

            return functools.partial(self.get, file_name, socket)

        # put
        if command == 2:
            file_name = receive_all(socket)

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
            try:
                command_code = int(receive_all(control_sock))
            except ValueError:
                print("[INFO] Attempting to exit gracefully....")

            print(f'received command code {command_code}')

            # each command is parsed  into a function that is invoked here
            # it will break when self becomes None after deletion
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
