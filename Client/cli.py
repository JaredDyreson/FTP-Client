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
    def __init__(self, server_name: str = "127.0.0.1", server_port: int = 0,
                 directory: pathlib.Path = pathlib.Path('/tmp/build')):
        if not(isinstance(server_name, str)
               and isinstance(server_port, int)
               and isinstance(directory, pathlib.Path)
               and directory.is_dir()):
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

    def ls(self):
        """lists the files located at the server"""
        # TODO: send the 'ls' command to the server over the 'control' channel
        # TODO: listen to the 'control' channel for the server's response
        # TODO: establish the 'data' channel
        # TODO: prepare to receive the output over the 'data' channel
        # TODO: close the 'data' channel
        # TODO: display the output

        print(f'ls [{self.directory}]')

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

    def parse_args(self, arguments: typing.List[str]) -> None:
        pass

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
            command = command.split(' ')

            if len(command) > 2:
                print('Too many arguments. Type \'help\' for the command list')
                continue

            if command[0] == 'get':
                if self.missing_arg(command):
                    continue
                self.get(command[1])
            elif command[0] == 'put':
                if self.missing_arg(command):
                    continue
                put(command[1], srvName, srvPort)
            elif command[0] == 'ls':
                self.ls()
            elif command[0] == 'help':
                self.cmd_list()
            elif command[0] == 'quit':
                # NOTE: we can just call __del__ and put implementation there
                # Note: we might need to listen to server response if we have to alert the server before disconnecting from it
                break
            else:
                print('Unknown command. Type \'help\' for the command list')


def main(argv: typing.List[str] = ["cli.py", "127.0.0.1", "0"]):
    if not(argv):
        argv = sys.argv
    if len(argv) != 3:
        print(
            f'Usage: python {argv[0]} <Server Domain Name> <Server Port>')

    server_name, server_port = argv[1:]
    try:
        server_port = int(server_port)
    except ValueError:
        print(
            f'[ERROR] Port should be number and non negative, received {server_port} of type {type(server_port)}')
        return

    cli = command_line_interface(
        server_name=server_name, server_port=server_port)
    cli.loop()


if __name__ == '__main__':
    main()
    # to have it use sys.argv, call `main([])`
