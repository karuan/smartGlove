# server.py

import socket
import select
import settings


HOST = '192.52.164.99'                 # Symbolic name meaning all available interfaces
PORT = 5000              # Arbitrary non-privileged port
NUM_CLIENTS = 1
MAX_TEAM_NO = 2


# message format
DELIM = ","
MSG_END = "!"
MSG_TEMP = "%s" + DELIM + "%s" + MSG_END

BUF_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client = [0]

s.bind((HOST, PORT))
s.listen(1)

global state;

def recv_and_parse(sock):
    try:
        data = sock.recvfrom(BUF_SIZE)[0]
        msgs = data.strip(MSG_END).split(MSG_END) 	# split messages
	ret_msgs = list()
	for msg in msgs:
            s = msg.split(DELIM) 					# split team num and command
            if len(s) != 2:
                print "packet malformed: " , s
                continue
            
            ret_msgs.append((s[0],s[1])) 			# packed into tuples
        return ret_msgs
            
    except socket.error:
	print("No data found")
	return None

def check_socks(socks):
    print socks
    for sock in socks:
        r,_,_ = select.select([sock],[],[],0)
        print r
        if r:
            print "found dead socket: ", r ," removing now"
            socks.remove(r)

            
##handshake
print "listening for connections"
conn, addr = s.accept()
message = conn.recv(1024)
print "Connected by", addr
client= [conn]
    

while True:
    global state;
    global distance;
    # this will block until at least one socket is ready
    r_ready_socks,_,_ = select.select(client, [], [])
    for sock in r_ready_socks:
        msgs = recv_and_parse(sock) # This is will not block
        distance=msgs[1];
        state[0]=(msgs[0]%10 == 1)
        state[1] = ((msgs[0]%100)/10 == 1)
        state[2] = ((msgs[0]%1000)/100 == 1)
        state[3] = (msgs[0]%1000 == 1)
        print "received message:", msgs, "from: ", sock
        if msgs is None:
            print "received empty packet"
            continue
conn.close()
