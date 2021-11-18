import socket


class SocketConnectionFailed(Exception):
    """Raised if the connection cannot be established to the server"""


class Socket:
    def __init__(self, server_name: str = "127.0.0.1", server_port: int = 1233):
        if not(isinstance(server_name, str)
               and isinstance(server_port)
               and (server_port > 0)):
            raise ValueError("something special")

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.connection.connect((self.server_name, self.server_port))
        except TimeoutError, InterruptedError:
            raise SocketConnectionFailed(
                f'cannot connect to the server {self.server_name} at port {self.server_port}')

    def send(self, information: str) -> None:
        if not(isinstance(information, str)):
            raise ValueError(
                f'function expected a `str`, obtained a {type(information)} instead')
        self.connection.send(information.encode('utf-8'))

    def deliver(self, *args, **kwargs):
        """TODO: this function should be communicating with client.receive_all"""
        raise NotImplementedError
