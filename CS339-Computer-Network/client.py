################
# Hongyuan Gao gao0927@gmail.com
# 2015.4.16
# server.py
# Python 2.7.6
################

import socket
import time
import thread
import sys
import os

# create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    # connect to the server
    addr = raw_input('Server Address: ')
    try:
        sock.connect((addr, 8001))
        break
    except:
        print 'Failed.'

time.sleep(2)

# receive welcome message
print sock.recv(1024)
sock.send('rpath')

l_path = sys.path[0] + '/client' # get or create local path
if not os.path.exists(l_path): os.mkdir(l_path)
r_path = sock.recv(1024) # remote path


while True:
    # show local and remote 
    print'------------------------------\nlocal: %s\nremote: %s\n------------------------------' % (l_path, r_path)

    # get command
    cmd = raw_input('client> ')

    # quit
    if cmd.split()[0] == 'quit':
        sock.send(cmd)
        print sock.recv(1024)
        sock.close()
        break

    # list local files and directories
    elif cmd.split()[0] == 'lsl':
        files = os.listdir(l_path)
        filelist = 'Filename' + '\t\t\t\t' + 'Size' + '\n'
        empty = True
        for f in files:
            if empty: empty = False
            fpath = l_path + '/' + f
            if os.path.isfile(fpath):
                filelist += f + '\t\t\t\t' + str(os.path.getsize(fpath)) + '\n'
            else:
                filelist += '<dir>' + f + '\n'
        if empty: filelist = '<Empty>'

        print filelist

    # list files and directories
    elif cmd.split()[0] == 'lsr':
        sock.send(cmd)
        print sock.recv(2048)

    # change local path
    elif cmd.split()[0] == 'cld':
        if len(cmd.split()) < 2:
            print 'Format: cld <dir name>'
            continue
        elif cmd.split()[1] == '..':
            if l_path == sys.path[0] + '\client': 
                pass
            else:
                tmp = l_path.split('/')
                l_path = l_path[0: len(l_path)-len(tmp[len(tmp)-1])-1]
        else:
            fpath = l_path = l_path + '/' + cmd.split()[1]
            if os.path.exists(fpath):
                l_path = fpath
            else:
                print 'No such directory.'

    # change remote path
    elif cmd.split()[0] == 'crd':
        if len(cmd.split()) < 2:
            print 'Format: crd <dir name>'
            continue
        sock.send(cmd)
        buf = sock.recv(1024)
        # path doesn't exist
        if buf[0] == '0':
            print 'No such directory.'
        else:
            r_path = buf[1:len(buf)]

    # create local dir
    elif cmd.split()[0] == 'mkldir':
        if len(cmd.split()) < 2:
            print 'Format: mkldir <dir name>'
            continue
        else:
            try:
                os.mkdir(l_path + '/' + cmd.split()[1])
                print 'Done.'
            except:
                print 'Failed.'

    # create remote dir
    elif cmd.split()[0] == 'mkrdir':
        if len(cmd.split()) < 2:
            print 'Format: mkrdir <dir name>'
            continue
        sock.send(cmd)
        print sock.recv(1024)


        
    # download file 
    elif cmd.split()[0] == 'get':
        if len(cmd.split()) < 2:
            print 'Format: get <filename>'
            continue
        else:
            sock.send(cmd)

            # file exists?
            if sock.recv(1) == '1':
                print 'No file named "%s".' % cmd.split()[1]
                continue

            # create file
            fp = open(l_path + '/' + cmd.split()[1], 'wb')

            #fsize = sock.recv(1024)
            while True:
                try:
                    sock.settimeout(2)
                    buf = sock.recv(1024)
                    fp.write(buf)
                except:
                    fp.close()
                    sock.setblocking(1)
                    break
            print 'Download finished'


    # upload file
    elif cmd.split()[0] == 'put':
        if len(cmd.split()) < 2:
            print 'Format: put <filename>'
            continue
        else:
            try:
                fp = open(l_path + '/' + cmd.split()[1], 'rb')
            except:
                print 'No file named "%s".' % cmd.split()[1]
                continue

            sock.send(cmd)
            while True:
                buf = fp.read(1024)
                if len(buf) == 0: 
                    break
                    #connection.send('EOF')
                else: sock.send(buf)
            print sock.recv(1024)
            
    

    # delete local file
    elif cmd.split()[0] == 'dell':
        if len(cmd.split()) < 2:
            print 'Format: dell <filename>'
            continue
        else:
            try:
                os.remove(l_path + '/' + cmd.split()[1])
            except:
                print 'Failed.'

    # delete remote file
    elif cmd.split()[0] == 'delr':
        if len(cmd.split()) < 2:
            print 'Format: delr <filename>'
            continue
        else:
            sock.send(cmd)
            print sock.recv(1024)

    # print command list
    elif cmd.split()[0] == 'help':
        print '************\nCommand List\n************'
        print 'quit\t\tClose the client.'
        print 'lsl\t\tList local files and directories.'
        print 'lsr\t\tList remote files and directories.'
        print 'cld <dir name>\t\tChange local path.'
        print 'crd <dir name>\t\tChange remote path.'
        print 'mkldir <dir name>\t\tCreate local directory.'
        print 'mkrdir <dir name>\t\tCreate remote directory.'
        print 'get <filename>\t\tDownload file.'
        print 'put <filename>\t\tUplaod file.'
        print 'dell <filename>\t\tDelete local file.'
        print 'delr <filename>\t\tDelete remote file'

    # invalid command
    else:
        print 'Invalid command. Type "help" for command list.'

