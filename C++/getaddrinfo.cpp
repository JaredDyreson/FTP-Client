#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>       /* for AF_INET */
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdio.h>


int main(int argc, char** argv)
{
	/* Check for errors */
	if(argc < 2)
	{
		fprintf(stderr, "USAGE: %s <DOMAIN NAME>\n", argv[0]);
		exit(-1);
	}
	
	/* The structure to store the resolved address 
	 * and the structure to store the head used for traversing
	 * linked list of structures.
	 */
	struct addrinfo* resolution = NULL;
	struct addrinfo* resolutionHead = NULL;
	
	/* Try to resolve the name to the IP */
	if(getaddrinfo(argv[1], NULL, NULL, &resolution) < 0)
	{
		perror("getaddrinfo");
		exit(-1);
	}

	
	
	/* Get the pointer to the list of IP addresses */
	struct sockaddr* addrsPtr = resolution->ai_addr;
	
	/* Print all IPs associated with a domain (could be more than 1) */
	for (resolutionHead = resolution; resolutionHead != NULL; resolutionHead = resolutionHead->ai_next)
	{
		/* Get the pointer to the IP address */
		addrsPtr = resolutionHead->ai_addr;
		
		/* Print the address in string format */
		fprintf(stderr, "IP: %s \n", inet_ntoa((((struct sockaddr_in *)addrsPtr)->sin_addr))); 
	}
	
	/* Free all addrinfo data structures */
	freeaddrinfo(resolution);
		
	return 0;
}
