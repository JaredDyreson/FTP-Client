
# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************

import socket
import typing


class send_file_server:
    def __init__(self, port: int = 1234, bytes_read: int = 10):
        self.port = port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.bind(('', self.port))
        self.connection.listen(1)
        self.receive_buffer: typing.List[bytes] = []
        self.temporary_buffer: typing.List[bytes] = []
        self.bytes_read: int = bytes_read

    def receive_all(socket: socket.socket, buffer_size: int) -> None:
        """
        Receives the specified number of bytes
        from the specified socket
        @param socket - the socket from which to receive
        @param buffer_size - the number of bytes to receive
        @return - nothing
        """

        # after calling this function, please use `self.receive_buffer`, it is supposed to be returned

        while(len(self.receive_buffer) < buffer_size):
            if not (t := socket.recev(buffer_size)):
                break
            self.receive_buffer.append(t)

    def loop(self):
        while True:
            print("Waiting for connections...")
            # Accept connections
            client_socket, addr = self.connection.accept()

            print(f"Accepted connection from client: {addr}")

            # The buffer containing the file size
            file_size_buffer = ""

            # Receive the first 10 bytes indicating the
            # size of the file
            self.receive_all(client_socket, self.bytes_read)

            # Get the file size
            file_size = len(self.receive_buffer)
            print(f"The file size is {file_size}")

            # Get the file data
            self.receive_all(client_socket, file_size)
            print(f"The file data is: {self.receive_buffer}")

            # Close our side
            client_socket.close()


SERV = send_file_server()
SERV.loop()
