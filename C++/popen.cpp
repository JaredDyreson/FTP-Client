#include <stdio.h>
#include <stdlib.h>
#include <string>
using namespace std;

FILE *popen(const char *command, const char *type);

/**
 * Returns the output of a command in C++ string format
 * @param cmd - the command to execute
 * @return - the output of the commaned in C++ format
 */
string getCmdOutput(const char* cmd)
{
	/* The buffer to store the results */
	string result = "";
	
	/* Open the output stream of the program for reading */
	FILE* fp = popen(cmd, "r");
	
	/* The output buffer */
	char outBuff[10];
	
	/* The number of bytes read */
	int numRead = 0;
	
	/* Make sure the stream was opened */
	if(!fp)
	{
		perror("popen");
		exit(-1);
	}
	
	/* Read the whole file */
	while(!feof(fp))
	{	
		/* Read information from the output stream of the program */
		if((numRead = fread(outBuff, sizeof(char), sizeof(outBuff) - 1, fp)) < 0)
		{
			perror("fread");
			exit(-1);
		}
			
		/* NULL terminate the string */
		outBuff[numRead] = '\0';	
	
		/* If anything was read, then save it! */
		if(numRead)
			result += outBuff;
		
	}
	
	/* Close the output stream of the program */
	if(pclose(fp) < 0)
	{
		perror("pclose");
		exit(-1);
	}
	
	return result;
	
}

int main(int argc, char** argv)
{

	/* Get the output of the ls command */
	string result =  getCmdOutput("ls");
	
	/* Print the output of the ls command */
	fprintf(stderr, "%s\n", result.c_str());	
	
	return 0;
}
