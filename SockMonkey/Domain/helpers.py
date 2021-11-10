import socket
import typing

def receive_bytes(socket: socket.socket, buffer_size: int) -> str:
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

def receive_all(socket: socket.socket) -> str:
    """
    Receive the entire message from socket.
    The first 10 bytes must indicate the size of the message.
    """
    try:
        if (size := int(receive_bytes(socket, 10))) < 0:
            return f'receive_all() received the wrong message format from {socket}. The message size was negative'
    except:
        return f'receive_all() received the wrong message format from {socket}. The first 10 bytes must be the message\'s size'

    return receive_bytes(socket, size)

def send_all(socket: socket.socket, msg: str, prepend: bool = True) -> None:
    """
    Sends msg encoded using utf-8 over socket.
    @prepend - msg should be prepended with its size (size is padded to 10 bytes)
    @return - the num of bytes sent
    """
    if prepend:
        msg = prepend_size(msg)
    
    bytes_sent = 0

    # keep sending until all the data is sent
    while len(msg) > bytes_sent:
        bytes_sent += socket.send(msg[bytes_sent:].encode('utf-8'))

def prepend_size(s: str) -> str:
    """Prepends a string with its size"""
    size = str(len(s))

    # first 10 bytes of a string will be its size e.g. 0000000004DONE
    size = pad_str(size)
       
    return size + s

def pad_str(s: str, pad: str = '0', length: int = 10) -> str:
    """
    Prepends a string to a desired length
    @pad - the charater to prepend the string with
    @length - the total length desired
    """
    while len(s) < length:
        s = pad + s
    return s