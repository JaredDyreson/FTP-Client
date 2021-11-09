"""
This file controls the ftp client
It receives commands from the user and sends/receives data to/from the server
"""


import os
import socket
import sys
import typing
import functools
import pathlib


class command_line_interface:
    def __init__(self, server_name: str = "127.0.0.1", server_port: int = 1233,
                 directory: pathlib.Path = pathlib.Path('/tmp/build')):
        if not(isinstance(server_name, str)
               and isinstance(server_port, int)
               and isinstance(directory, pathlib.Path)):
            #       and directory.is_dir()):
            raise ValueError(
                f'mismatched constructor: command_line_interface({list(locals().values())[1:]})')
        self.server_name = server_name
        self.server_port = server_port
        self.directory = directory

    def get(self, file_name: str) -> None:
        """requests a file from the server"""
        # TODO: send the 'get' command to the server over the 'control' channel
        # TODO: listen to the 'control' channel for the server's response
        # TODO: establish the 'data' channel
        # TODO: prepare to receive the file's data over the 'data' channel
        # TODO: close the 'data' channel
        # TODO: write the data to a new file

        print(f'get [{file_name}]')

    def put(self, file_name: str) -> None:
        """sends a file to the server"""
        # TODO: establish the 'data' channel
        # TODO: send the file's data to the server over the 'data' channel
        # TODO: listen to the 'control' channel for the server's response
        # TODO: close the 'data' channel

        print(f'put [{file_name}]')

    def ls(self) -> None:
        """lists the files located at the server"""
        # Temporary: the connection should be established outside of this function
        conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            conn_socket.connect((self.server_name, self.server_port))
        except:
            print('there is no server. this should not work')
            return

        # send the 'ls' command to the server over the 'control' channel
        cmd_str = '1'
        conn_socket.send(cmd_str.encode('utf-8'))

        # receive the server's response. it should be 10 bytes and contain the the port number for the 'data' channel
        print("Waiting for server response...")
        data_port = int(self.receive_all(conn_socket, 10))
        print(f'Connecting to the server on port {data_port}')

        # connect to the server over 'data'
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((self.server_name, data_port))

        # receive the output over the 'data' channel
        response_size = int(self.receive_all(data_socket, 10))
        file_list: str = self.receive_all(data_socket, response_size)

        # close the 'data' channel
        data_socket.close()

        # display the output
        print(file_list)

        # print(f'ls [{self.directory}]')

    def receive_all(socket: socket.socket, buffer_size: int) -> str:
        """
        Receives the specified number of bytes
        from the specified socket
        @param socket - the socket from which to receive
        @param buffer_size - the number of bytes to receive
        @return - string
        """
        receiver_buffer: typing.List[bytes] = []
        while len(receiver_buffer) < buffer_size:
            if not (t := socket.recev(buffer_size)):
                break
            receiver_buffer.append(t)
        return receiver_buffer.decode('utf-8')

    def missing_arg(self, cmd: typing.List[str]) -> bool:
        """checks get and put commands for a missing argument"""
        # NOTE: changed to just see if the length of the command is either 0 or 1
        return 0 <= len(cmd) <= 1

    def cmd_list(self) -> None:
        """prints out the list of available commands"""
        print('get [file name]')
        print('put [file name]')
        print('ls')
        print('help')
        print('quit')

    def __del__(self):
        """clean up the object once we're done"""
        # TODO: close port
        # terminate connection

        print(f"deleting object at {self}")

    def parse_args(self, arguments: typing.List[str]) -> typing.Callable:
        def empty(): return None  # void function

        if len(arguments) > 2:
            print('Too many arguments. Type \'help\' for the command list')
            return empty

        prefix = arguments[0]

        if prefix == 'get' and not self.missing_arg(arguments):
            return functools.partial(self.get, arguments[1])

        if prefix == 'put' and not self.missing_arg(arguments):
            return functools.partial(self.put, arguments[1])

        if prefix == 'ls':
            return self.ls

        if prefix == "help":
            return self.cmd_list

        if prefix == 'quit':
            # NOTE: we can just call __del__ and put implementation there
            # Note: we might need to listen to server response if we have to alert the server before disconnecting from it
            return self.__del__
        else:
            print('Unknown command. Type \'help\' for the command list')
            return empty

    def loop(self):
        """receives and executes commands on loop"""
        # Note: loop might continue while the command is being executed. I've never done this so I wouldn't know.
        # TODO: we could open/close the 'control' channel here and send the variable to each command function
        #       OR we could have variable be global and open/close it in main()
        #       OR we could open/close the channel in each command functuion (I feel like this way is wrong though)

        while True:
            try:
                command = input('ftp> ')
            except EOFError:
                # treat as quit
                break

            # input is split per word and inserted into an array. It becomes like argv
            # each command is parsed  into a function that is invoked here
            self.parse_args(command.split(' '))()


def main(argv: typing.List[str] = ["cli.py", "127.0.0.1", "1234"]):
    if not(argv):
        argv = sys.argv
    if len(argv) != 3:
        print(
            f'Usage: python {argv[0]} <Server Domain Name> <Server Port>')

    server_name, server_port = argv[1:]
    try:
        if((server_port := int(server_port)) < 0):
            print(
                f"[ERROR] Port number should not be negtive, received {server_port}")
            return
    except ValueError:
        print(
            f'[ERROR] Port should be number, received {server_port} of type {type(server_port)}')
        return

    cli = command_line_interface(
        server_name=server_name, server_port=server_port)
    cli.loop()
