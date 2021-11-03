#include <stdio.h>      /* Contains common I/O functions */
#include <sys/types.h>  /* Contains definitions of data types used in system calls */
#include <sys/socket.h> /* Includes definitions of structures needed for sockets */
#include <netinet/in.h> /* Contains constants and structures needed for internet domain addresses. */
#include <unistd.h>     /* Contains standard unix functions */
#include <stdlib.h>     /* For atoi() and exit() */
#include <string.h> 	/* For memset() */


int main(int argc, char** argv)
{
	/* The integer to store the file descriptor number
	 * which will represent a socket on which the server
	 * will be listening
	 */
	int listenfd = -1;
	
	/* The file descriptor representing the connection to the client */
	int connfd = -1;
	
	/* The structures representing the server and client
	 * addresses respectively
	 */
	sockaddr_in serverAddr, cliAddr;
		
	/* The address where the random port is stored */
	sockaddr_in randomPortAddr;
	
	/* Stores the size of the client's address */
	socklen_t cliLen = sizeof(cliAddr);		
	
	
	
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
		
	/*** 
	  * THIS IS THE KEY STEP IN ORDER TO
	  * GET AN EPHEMERAL PORT: CALL BIND
	  * WITH PORT ARGUMENT SET TO 0.
	  * THIS WILL BIND THE SOCKET TO THE 
	  * FIRST AVAILABLE PORT. WE CAN LATER
	  * FIND OUT WHAT THAT PORT NUMBER IS 
	  * SEE BELLOW.
	  */	
	serverAddr.sin_port = htons(0);
	
	/* Set the server family */
	serverAddr.sin_family = AF_INET;
	
	/* Retrieve packets without having to know your IP address,
	 * and retrieve packets from all network interfaces if the
	 * machine has multiple ones
	 */
	serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);
	
	/* Get the size of the address field */
	socklen_t addrSize = sizeof(serverAddr);
		
	/* Associate the address with the socket */
	if(bind(listenfd, (struct sockaddr *)&serverAddr, addrSize) < 0)
	{
		perror("bind");
		exit(-1);
	}
		
	/** 
	 * RETRIEVE THE RANDOM PORT NUMBER PICKED BY BIND
	 */
	if(getsockname(listenfd, (struct sockaddr*)&randomPortAddr, &addrSize) < 0)
	{
		perror("getsockname");
		exit(-1);
	}
		
	/* Print the port number */	
	fprintf(stderr, "Port  = %d\n", ntohs(randomPortAddr.sin_port)); 	
		
	/* Listen for connections on socket listenfd.
	 * allow no more than 100 pending clients.
	 */
	if(listen(listenfd, 100) < 0)
	{
		perror("listen");
		exit(-1);
	}
	

	/* A structure to store the client address */
	if((connfd = accept(listenfd, (sockaddr *)&cliAddr, &cliLen)) < 0)
	{
		perror("accept");
		exit(-1);
	}

	/* Client connected */
	fprintf(stderr, "Client connected\n");
	
	/* Close the socket */
	close(connfd);
	
	return 0;
}



