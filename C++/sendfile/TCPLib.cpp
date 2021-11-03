/**
 * Implements TCPLib
 */

#include "TCPLib.h"

/*
 * Keeps transmitting a buffer until the buffer is transmitted
 * @param socket - the socket to use for sending
 * @param buffer - the buffer to send
 * @param buffSize - the size of the buffer
 * @return - the number of bytes transmitted, or -1 on error 
 */
int tcp_send(const int& socket, const void* buffer, const int& buffSize)
{
	/* @numSent - the number of bytes sent in one shot
	 * @totalBytesSent - the cumulative number of bytes sent
	 */
	int numSent = 0, totalBytesSent = 0;
	
	/* Keep transmitting until all is transmitted */
	while(totalBytesSent != buffSize)
	{
		/* Transmit the buffer */
		if((numSent = write(socket, (char*)buffer + totalBytesSent, buffSize - totalBytesSent)) < 0)
		{
			/* Something went wrong while transmitting */
			return numSent;
		}
		
		/* Update the total number of bytes sent */
		totalBytesSent += numSent;
	}
		
	/* Successful transmission */	
	return totalBytesSent;
}


/**
 * Keeps receiving a buffer until all bytes are received
 * @param socket - the socket to use for receiving
 * @param buffer - the buffer to send
 * @param buffSize - the size of the buffer
 * @return - the number of bytes received, or -1 on error 
 */
int tcp_recv(const int& socket, void* buffer, const int& buffSize)
{

	/* @numRecv - the number of bytes received in one shot
	 * @totalBytesRecv - the cumulative number of bytes received
	 */
	int numRecv = 0, totalBytesRecv = 0;
	
	/* Keep transmitting until all is transmitted */
	while(totalBytesRecv != buffSize)
	{
		/* Transmit the buffer */
		if((numRecv = read(socket, (char*)buffer + totalBytesRecv, buffSize - totalBytesRecv)) < 0)
		{
			/* Something went wrong while receiving */
			return numRecv;
		}
		
		/* Update the total number of bytes receiving */
		totalBytesRecv += numRecv;
	}
	
	/* Successful reception */
	return totalBytesRecv;
}



/**
 * Stringifies an integer, saves it into array of
 * size SIZE_MSG_SIZE, and sends it over the socket
 * @return - SIZE_MSG_SIZE on success, -1 on failure
 */
int tcp_send_size(const int& socket, const int& size)
{
	/* The buffer to store the stringified size */
	char size_buff[SIZE_MSG_SIZE];
	
	/* Convert the integer to string, and get the number of
	 * characters in the resulting conversion. NOTE: if
	 * the size is more than SIZE_MSG_SIZE digits, then
	 * this function will truncate the number.
	 */
	if(snprintf(size_buff, SIZE_MSG_SIZE, "%d", size) < 0)
		return -1;
	
	
	/* Send the size */
	return tcp_send(socket, size_buff, SIZE_MSG_SIZE);	
}

/** 
 * Receives size. Assumes the size of the message containing the
 * size is SIZE_MSG_SIZE. The message is then converted from string
 * to integer, and returns the size
 * @param socket - the socket to receive the size from
 * @return - the size, or -1 on error
 */
int tcp_recv_size(const int& socket)
{
	/* The buffer to store the size */
	char size_buff[SIZE_MSG_SIZE + 1];
	
	/* The number of bytes received */
	int numRecv = -1;
			

	/* Receive the size */
	if((numRecv = tcp_recv(socket, size_buff, SIZE_MSG_SIZE)) < 0)
	{
		/* Something went wrong */
		return numRecv;	
	}
	
	/* NULL terminate the received size */
	size_buff[numRecv] = '\0';
	
	/* Convert the string to integer, and we are done */
	return atoi(size_buff);
}
