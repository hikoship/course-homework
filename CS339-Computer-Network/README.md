# Lecturer
[Liping Shen](http://www.cs.sjtu.edu.cn/PeopleDetail.aspx?id=83)

# Socket Programming - File Share Client/Server

## Introduction
### System Function
The system includes three Python files server.py client.py and ftp.py. server.py and client.py can run on two different computers (or both on the same one), and then the client can implement the following functions:

* Show current path of client and server
* List the objects in the current directory of client or server with file size.* Change current directory of client or server* Create a directory on client or server* Download files from server* Upload files to server* Delete files on server

### Runtime Environment
* Dev OS: Mac OS X 10.10
* Language: Python 2.7.6
The system are tested to run well on the following situations:
* Server and client run on one computer with Mac OS X 10.10
* Server and client run on two computers under a subnet, server with Ubuntu 14.04 and client with Mac OS X 10.10## System  Design
### Architecture
The server creates a socket, binds it with its address and a given port 8001, and then listens con- nection from clients. Here it uses a blocking *accept()* method to wait for connection. While if a client launches, it also creates a socket, and tries to connect to the the IP and port provided by the user.The socket exchanges data by *send()* and *recv()*. When the client want to download a file, the command it sends will be analysized, which leads the server to open the concerned file in bi- nary. It uses a for loop to send the file with 1KB per time. At the same time, the client open a file also in binary, continually reading data from socket in 1KB. If *recv()* method waited data for 2 seconds, it triggered *settimeout()* (which means the server has read all the file) and stops receiving then closed it.
Other operations such as list objects, change directory, create directory and delete files are all implemented by os and sys library.
### File Discription
* ***server.py***: Source file to launch a server.
* ***client.py***: Source file to launch a client.
## How to Use
Install Python 2, and then run it in terminal.
### server.py
Run **server.py**, and the server will automatically establish. When a client connects or disconnects, it prints a message.
### client.py
Run client.py, then type server address. If you run server and client on a same computer, just type "localhost" or "127.0.0.1". Otherwise, enter the IP address of computer on which the server runs.The client accepts the following commands:
* ***quit***: Quit the client* ***lsl***: List local objects* ***lsr***: List remote objects* ***cld \<dir name>***: Change local path* ***crd \<dir name>***: or crd ..: Change remote path
* ***mkldir <dir name>: Create local directory* ***mkrdir <dir name>: Create remote directory* ***get <filename>: Download files from server* ***put <filename>: Upload files to server