/**
 * Declares functions useful for transmitting
 * and receiving information using TCP.
 */

#ifndef TCP_LIB
#define TCP_LIB

#include <stdio.h>      /* Contains common I/O functions */
#include <sys/types.h>  /* Contains definitions of data types used in system calls */
#include <sys/socket.h> /* Includes definitions of structures needed for sockets */
#include <netinet/in.h> /* Contains constants and structures needed for internet domain addresses. */
#include <unistd.h>     /* Contains standard unix functions */
#include <stdlib.h>     /* For atoi() and exit() */
#include <string.h> 	/* For memset() */
#include <arpa/inet.h>  /* For inet_pton() */
#include <time.h>       /* For retrieving the time */
#include <limits.h>	/* For the maximum integer size */
#include <cstdlib>  
#include <cstddef>

/* The size of the buffer size message */
#define SIZE_MSG_SIZE 100

/**
 * Keeps transmitting a buffer until the buffer is transmitted
 * @param socket - the socket to use for sending
 * @param buffer - the buffer to send
 * @param buffSize - the size of the buffer
 * @return - the number of bytes transmitted, or -1 on error 
 */
int tcp_send(const int& socket, const void* buffer, const int& buffSize);


/**
 * Keeps receiving a buffer until all bytes are received
 * @param socket - the socket to use for sending
 * @param buffer - the buffer to send
 * @param buffSize - the size of the buffer
 * @return - the number of bytes transmitted, or -1 on error 
 */
int tcp_recv(const int& socket, void* buffer, const int& buffSize);


/**
 * Stringifies an integer, saves it into array of
 * size SIZE_MSG_SIZE, and sends it over the socket
 * @return - SIZE_MSG_SIZE on success, -1 on failure
 */
int tcp_send_size(const int& socket, const int& size);

/** 
 * Receives size. Assumes the size of the message containing the
 * size is SIZE_MSG_SIZE. The message is then converted from string
 * to integer, and returns the size
 * @param socket - the socket to receive the size from
 * @return - the size, or -1 on error
 */
int tcp_recv_size(const int& socket);

#endif
