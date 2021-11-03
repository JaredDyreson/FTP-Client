all:	getaddrinfo getephport popen sendfile

getaddrinfo:	getaddrinfo.cpp
	g++ getaddrinfo.cpp -o getaddrinfo

getephport:	getephport.cpp
	g++ getephport.cpp -o getephport

popen:	popen.cpp
	g++ popen.cpp -o popen

sendfile::	
	make -C sendfile/

clean:
	rm -rf getaddrinfo getephport popen
	make -C sendfile/ clean
