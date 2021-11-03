#include <stdio.h>      /* Contains common I/O functions */
#include <sys/types.h>  /* Contains definitions of data types used in system calls */
#include <sys/socket.h> /* Includes definitions of structures needed for sockets */
#include <netinet/in.h> /* Contains constants and structures needed for internet domain addresses. */
#include <unistd.h>     /* Contains standard unix functions */
#include <stdlib.h>     /* For atoi() and exit() */
#include <string.h> 	/* For memset() */
#include <time.h>       /* For retrieving the time */
#include <limits.h>	/* For limits */
#include "TCPLib.h"     /* For tcp_recv, tcp_recv_size, tcp_send_size, and tcp_send */


/* The maximum size of the file chunk */
#define MAX_FILE_CHUNK_SIZE 100

/**
 * Returns the smallest of the two integers
 * @param fInt - the first integer
 * @param sInt - the second integer
 * @return - the smallest of the two integers
 */
int min(const int& fInt, const int& sInt)
{
	/* Find the smallest integer */
	if(fInt < sInt) return fInt;
	
	return sInt;
}

/**
 * Receives the file name from the specified socket
 * @param socket - the socket
 * @param fileName - the file name
 */
void recvFileName(const int& socket, char* fileName)
{
	
	/* The file name size */
	int fileNameSize = -1;
	
	/* Get the size of the file name */
	if((fileNameSize = tcp_recv_size(socket)) < 0)
	{
		perror("tcp_recv_size");
		exit(-1);
	}
	
	/* Get the file name */	
	if(tcp_recv(socket, fileName, fileNameSize) < 0)
	{
		perror("tcp_recv");
		exit(-1);
	}
	
	/* NULL terminate the file name */
	fileName[fileNameSize] = '\0';	
}

/* The maximum file name size */
#define MAX_FILE_NAME_SIZE 100

int main(int argc, char** argv)
{
	/* The port number */	
	int port = -1;
	
	/* The integer to store the file descriptor number
	 * which will represent a socket on which the server
	 * will be listening
	 */
	int listenfd = -1;
	
	/* The file descriptor representing the connection to the client */
	int connfd = -1;
	
	/* The size of the time buffer */
	#define TIME_BUFF_SIZE 100
	
	/* The buffer used for receiving data from the server */
	char recvBuff[MAX_FILE_CHUNK_SIZE];
	
	/* The  */
	char fileName[MAX_FILE_NAME_SIZE];
	
	/* The file size */
	int fileSize = 0;
	
	/* The number of bytes received */
	int numRead = 0;	
		
	/* The pointer to the output file */
	FILE* fp;
			
	/* The structures representing the server and client
	 * addresses respectively
	 */
	sockaddr_in serverAddr, cliAddr;
	
	/* Stores the size of the client's address */
	socklen_t cliLen = sizeof(cliAddr);	
	
	/* Make sure the user has provided the port number to
	 * listen on
	 */
	if(argc < 2)
	{
		/* Report an error */
		fprintf(stderr, "USAGE: %s <PORT #>", argv[0]);
		exit(-1);	
	}
	
	/* Get the port number */
	port = atoi(argv[1]);
	
	/* Make sure that the port is within a valid range */
	if(port < 0 || port > 65535)	
	{
		fprintf(stderr, "Invalid port number\n");
		exit(-1);
	} 
	
	/* Print the port number */	
	fprintf(stderr, "Port  = %d\n", port); 	
	
	/* Create a socket that uses
	 * IPV4 addressing scheme (AF_INET),
	 * Supports reliable data transfer (SOCK_STREAM),
	 * and choose the default protocol that provides
	 * reliable service (i.e. 0); usually TCP
	 */
	if((listenfd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
	{
		perror("socket");
		exit(-1);
	}
	
	
	/* Set the structure to all zeros */
	memset(&serverAddr, 0, sizeof(serverAddr));
		
	/* Convert the port number to network representation */	
	serverAddr.sin_port = htons(port);
	
	/* Set the server family */
	serverAddr.sin_family = AF_INET;
	
	/* Retrieve packets without having to know your IP address,
	 * and retrieve packets from all network interfaces if the
	 * machine has multiple ones
	 */
	serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);
	
	/* Associate the address with the socket */
	if(bind(listenfd, (sockaddr *) &serverAddr, sizeof(serverAddr)) < 0)
	{
		perror("bind");
		exit(-1);
	}
	
	/* Listen for connections on socket listenfd.
	 * allow no more than 100 pending clients.
	 */
	if(listen(listenfd, 100) < 0)
	{
		perror("listen");
		exit(-1);
	}
	
	/* Wait forever for connections to come */
	while(true)
	{
		
		fprintf(stderr, "Waiting for somebody to connect on port %d\n", port);
				
		/* A structure to store the client address */
		if((connfd = accept(listenfd, (sockaddr *)&cliAddr, &cliLen)) < 0)
		{
			perror("accept");
			exit(-1);
		}
		
			
		fprintf(stderr, "Connected!\n");
		
		/* Reset the number of bytes to read */
		numRead = 0;
		
		
		/* Get the file name size */
		recvFileName(connfd, fileName);
			
		
		/* Get the file size */
		if((fileSize = tcp_recv_size(connfd)) < 0)
		{
			perror("tcp_recv_size");
			exit(-1);
		}
		
			
		fprintf(stderr, "Receiving file: %s (%d bytes)...\n", fileName, fileSize);	
			
		/* Open the file */
		fp = fopen(fileName, "w");

		/* Error checks */
		if(!fp)
		{
			perror("fopen");
			exit(-1);
		}
		
		/* Keep receiving until the whole file is received */
		while(fileSize != 0)
		{
			/* Receive the chunk */
			if((numRead = tcp_recv(connfd, recvBuff, min(MAX_FILE_CHUNK_SIZE, fileSize))) < 0)
			{
				perror("tcp_recv");
				exit(-1);
			}	
			
			/* Save the received buffer */
			if(fwrite(recvBuff, sizeof(char), numRead, fp) < 0)
			{
				perror("fwrite");
				exit(-1);
			}
			
			/* Reduce the file size */
			fileSize -= numRead;
		}
		
		
		/* Close the socket */
		close(connfd);
		
		/* Close the file */
		fclose(fp);
	}	
		
		
	return 0;
}





