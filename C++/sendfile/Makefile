all: client server

client:	client.cpp TCPLib.o
	g++ client.cpp TCPLib.o -o client

server: server.cpp TCPLib.o
	g++ server.cpp TCPLib.o -o server

TCPLib.o:	TCPLib.h TCPLib.cpp
	g++ -c TCPLib.cpp 

clean:
	rm -rf server client TCPLib.o 
