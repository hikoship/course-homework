################
# Hongyuan Gao gao0927@gmail.com
# 2015.4.16
# server.py
# Python 2.7.6
################

import socket
import time
import os
import sys

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind
s.bind(('', 8001))
s.listen(5)

print 'Server established'

while True:
    sock,address = s.accept()
    print 'A client connected' 
    sock.send('Welcome!')

    # get or create server path
    s_path = sys.path[0] + '/server'
    if not os.path.exists(s_path): os.mkdir(s_path)

    if sock.recv(1024) == 'rpath':
        sock.send(s_path)
        
    #sock.settimeout(5)

    while True:
        cmd = sock.recv(1024)

        # error from client
        if cmd == '':
            sock.close()
            print 'a client disconnected'
            break
        
        # client quited
        if cmd.split()[0] == 'quit':
            sock.send('Bye')
            sock.close()
            print 'a client disconnected'
            break

        # list remote files and directories
        elif cmd.split()[0] == 'lsr':
            files = os.listdir(s_path)
            filelist = 'Filename' + '\t\t\t\t' + 'Size' + '\n'
            empty = True
            for f in files:
                if empty: empty = False
                fpath = s_path + '/' + f
                if os.path.isfile(fpath):
                    filelist += f + '\t\t\t\t' + str(os.path.getsize(fpath)) + '\n'
                else:
                    filelist += '<dir>' + f + '\n'
            if empty: filelist = '<Empty>'

            sock.send(filelist)

        # change remote path
        elif cmd.split()[0] == 'crd':
            # go back to parent directory
            status = '1' # path exists
            if cmd.split()[1] == '..':
                if s_path == sys.path[0] + '/server': 
                    pass
                else:
                    tmp = s_path.split('/')
                    s_path = s_path[0: len(s_path)-len(tmp[len(tmp)-1])-1]
            
            else:
                fpath = s_path + '/' + cmd.split()[1]
                if os.path.exists(fpath):
                    s_path = fpath
                else:
                    status = '0' # path doesn't exist

            sock.send(status + s_path)

        # create remote dir
        elif cmd.split()[0] == 'mkrdir':
            try:
                os.mkdir(s_path + '/' + cmd.split()[1])
                sock.send('Done.')
            except:
                sock.send('Failed.')

        # download file
        elif cmd.split()[0] == 'get':
            #sock.send(str(os.path.getsize(fpath)))

            try:
                fp = open(s_path + '/' + cmd.split()[1], 'rb')
                sock.send('0')
            except:
                # no such file
                sock.send('1')
                continue

            while True:
                buf = fp.read(1024)
                if len(buf) == 0: 
                    fp.close()
                    break
                else: sock.send(buf)

        # upload file
        elif cmd.split()[0] == 'put':
            fp = open(s_path + '/' + cmd.split()[1], 'wb')
            while True:
                try:
                    sock.settimeout(2)
                    buf = sock.recv(1024)
                    fp.write(buf)
                except:
                    fp.close()
                    sock.setblocking(1)
                    break
            sock.send('Upload finished')


        # delete file
        elif cmd.split()[0] == 'delr':
            try:
                os.remove(s_path + '/' + cmd.split()[1])
                sock.send('Done.')
            except:
                sock.send('Failed.')

        else:
            sock.send('please go out!')

