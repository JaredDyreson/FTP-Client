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

from SockMonkey.Domain.Client.helpers import receive_all, send_all


class command_line_interface:
    def __init__(self, server_name: str = "127.0.0.1", server_port: int = 1233,
                 directory: pathlib.Path = pathlib.Path.cwd()):
        if not(isinstance(server_name, str)
               and isinstance(server_port, int)
               and isinstance(directory, pathlib.Path)):
            raise ValueError(
                f'mismatched constructor: command_line_interface({list(locals().values())[1:]})')
        self.server_name = server_name
        self.server_port = server_port
        self.directory = directory
        self.control = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.control.connect((self.server_name, self.server_port))
        except:
            print(
                f'{self.server_name} on port {self.server_port} not found. Make sure to run the server before the client.')
            sys.exit(1)

    def get(self, file_name: str) -> int:
        """requests a file from the server"""
        # send the 'get' command and file name to the server over the 'control' channel
        send_all(self.control, '1')
        send_all(self.control, file_name)

        # listen to the 'control' channel for the server's response
        response = receive_all(self.control)
        if response == 'ERR':
            err_msg = receive_all(self.control)
            print(f'[SERVER ERROR] {err_msg}')
            return

        print("Receiving the data port number...")
        data_port = int(receive_all(self.control))

        print(f'Connecting to the server on port {data_port}...')
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((self.server_name, data_port))

        # receive the output over the 'data' channel
        print(f'Receiving [{file_name}]...')
        file_content: str = receive_all(data_socket)


        print(f'Writing...')
        with open(file_name, "w") as fp:
            fp.writelines(file_content)

        print(f'[{file_name}] has been written to {self.directory}')

        # close the 'data' channel
        data_socket.close()

    def put(self, file_name: str) -> int:
        """sends a file to the server"""

        # check if the file exists in the current dir
        if not pathlib.Path(f'{self.directory}/{file_name}').is_file():
                err_msg = (
                    f'[Client ERROR] File {file_name} does not exist. '
                    f'Path = {self.directory}'
                )
                print(err_msg)
                return


        # .basename() is in case file_name is a path to a file
        # send command code and file name
        send_all(self.control, '2')
        send_all(self.control, os.path.basename(file_name))

        # listen to the 'control' channel for the server's response
        response = receive_all(self.control)

        if response == 'ERR':
            err_msg = receive_all(self.control)
            print(f'[SERVER ERROR] {err_msg}')
            return

        print("Receiving the data port number...")
        data_port = int(receive_all(self.control))

        print(f'Connecting to the server on port {data_port}...')
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((self.server_name, data_port))

        print(f'Reading [{file_name}]...')
        with open(file_name, "r") as fp:
            contents = ''.join(fp.readlines())
        
        print(f'Sending...')
        send_all(data_socket, contents)

        print(f'[{file_name}] has been sent!')

        data_socket.close()

    def ls(self) -> int:
        """lists the files located at the server"""
        # send the 'ls' command to the server over the 'control' channel
        send_all(self.control, '3')

        # server responds with OK if there are no errors
        response = receive_all(self.control)
        if response == 'ERR':
            err_msg = receive_all(self.control)
            print(f'[SERVER ERROR] {err_msg}')
            return

        # receive the data port num
        print("Receiving the data port number...")
        data_port = int(receive_all(self.control))

        # connect to the server over 'data'
        print(f'Connecting to the server on port {data_port}...')
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((self.server_name, data_port))


        # receive the output over the 'data' channel
        print("Receiving the file list...")
        file_list: str = receive_all(data_socket)

        print("Receiving the list's directory...")
        server_dir: str = receive_all(data_socket)

        # close the 'data' channel
        data_socket.close()

        # display the output
        print(f'[INFO] Server path = {server_dir}')
        print(file_list)

    def missing_arg(self, cmd: typing.List[str]) -> bool:
        """checks get and put commands for a missing argument"""
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
        # tell the server to shut down
        try:
            send_all(self.control, '4')
        except BrokenPipeError:
            # server is not running but client is
            pass

        # terminate connection
        self.control.close()

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
            del self
        else:
            print('Unknown command. Type \'help\' for the command list')
            return empty

    def loop(self):
        """receives and executes commands on loop"""
        while True:
            try:
                command = input('ftp> ')
            except (EOFError, KeyboardInterrupt):
                # treat as quit
                break

            # input is split per word and inserted into an array. It becomes like argv
            # each command is parsed  into a function that is invoked here
            # it will break when self becomes None after deletion
            try:
                self.parse_args(command.split(' '))()
            except TypeError:
                break


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
    print('DONE')


if __name__ == '__main__':
    main()
    # to have it use sys.argv, call `main([])`
