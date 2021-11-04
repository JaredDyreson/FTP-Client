"""
This file controls the ftp client
It receives commands from the user and sends/receives data to/from the server
"""


import socket
import os
import sys


def get(fName, sName, sPort):
    """requests a file from the server"""
    # TODO: send the 'get' command to the server over the 'control' channel
    # TODO: listen to the 'control' channel for the server's response
    # TODO: establish the 'data' channel
    # TODO: prepare to receive the file's data over the 'data' channel
    # TODO: close the 'data' channel
    # TODO: write the data to a new file
    print('get', fName, sName, sPort)

def put(fName, sName, sPort):
    """sends a file to the server"""
    # TODO: establish the 'data' channel
    # TODO: send the file's data to the server over the 'data' channel
    # TODO: listen to the 'control' channel for the server's response
    # TODO: close the 'data' channel
    print('put', fName, sName, sPort)

def ls(sName, sPort):
    """lists the files located at the server"""
    # TODO: send the 'ls' command to the server over the 'control' channel
    # TODO: listen to the 'control' channel for the server's response
    # TODO: establish the 'data' channel
    # TODO: prepare to receive the output over the 'data' channel
    # TODO: close the 'data' channel
    # TODO: display the output
    print('listing files...', sName, sPort)

def missing_arg(cmd):
    """checks get and put commands for a missing argument"""
    try:
        if cmd[1] != '':
            # argument exits and is not blank
            return False
    except IndexError:
        pass

    print('Missing argument. Type \'help\' for the command list')
    return True

def cmd_list():
    """prints out the list of available commands"""
    print('get [file name]')
    print('put [file name]')
    print('ls')
    print('help')
    print('quit')

def command(srvName, srvPort):
    """receives and executes commands on loop"""
    # Note: loop might continue while the command is being executed. I've never done this so I wouldn't know.
    # TODO: we could open/close the 'control' channel here and send the variable to each command function
    #       OR we could have variable be global and open/close it in main()
    #       OR we could open/close the channel in each command functuion (I feel like this way is wrong though)

    while True:
        command = input('ftp> ')

        # input is split per word and inserted into an array. It becomes like argv
        command = command.split(' ')
        
        if len(command) > 2:
            print('Too many arguments. Type \'help\' for the command list')
            continue
        
        if command[0] == 'get':
            if missing_arg(command):
                continue
            get(command[1], srvName, srvPort)
        elif command[0] == 'put':
            if missing_arg(command):
                continue
            put(command[1], srvName, srvPort)
        elif command[0] == 'ls':
            ls(srvName, srvPort)
        elif command[0] == 'help':
            cmd_list()
        elif command[0] == 'quit':
            # Note: we might need to listen to server response if we have to alert the server before disconnecting from it
            break
        else:
            print('Unknown command. Type \'help\' for the command list')

def main():
    if len(sys.argv) != 3:
        print("Usage: python " + sys.argv[0] + " <Server Domain Name> " + "<Server Port>")
        return
    
    serverName = sys.argv[1]
    serverPort = sys.argv[2]

    # check if server port number is valid
    try:
        serverPort = int(serverPort)
        if serverPort < 0:
            # raise error if port num is negative
            int('a')
    except ValueError:
        print('Error: Port number is invalid. It must be a positive integer')
        return

    command(serverName, serverPort)
    print('end of main')

if __name__ == '__main__':
    main()