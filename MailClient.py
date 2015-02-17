_author_ = "Shovik Shyamsundar"

from socket import *

server = gethostname()

socket = socket(AF_INET, SOCK_STREAM)
port = 25

#Creates socket and establishes TCP connection
socket.connect(('', port))

#Checks server response
msg = socket.recv(1024)
if msg[:3] != "220":
    print "220 reply not received from server."
else:
    print "220 " + server + " service ready."

#Asks for sender's email
print "Sender's email:"
sender = raw_input()
socket.send("MAIL FROM: <" + sender + ">\r\n")

#Checks server reponse
msg = socket.recv(1024)
if msg[:3] != "250":
    print "250 reply not received from server."
else: 
    print "250 OK"

#Asks for recipient's email
print "Recipient's email:"
rcpt = raw_input()
socket.send("RCPT TO: <" + rcpt + ">\r\n")

msg = socket.recv(1024)

#Server accepts recipient address
if msg[:3] == "250":
    print "250 OK"
    socket.send("DATA\r\n")
    msg2 = socket.recv(1024)
    if msg2[:3] != "354":
        print "354 reply not received from server."

    #Sends sender and recipient to server
    socket.send("To: " + rcpt + "\n")
    socket.send("From: " + sender + "\n")

    #Asks for subject
    print "Enter Subject:"
    subject = raw_input()
    socket.send("Subject: " + subject + "\n")

    #Asks for message
    print "Compose message (end message with \".\"):"
    while 1:
        msg2 = raw_input()
        if msg2 == ".":
            break
        socket.send(msg2 + "\r\n")

    socket.send("\r\n.\r\n")

    #Checks server response
    msg2 = socket.recv(1024)
    if msg2[:3] == "250":
        print "250 OK"
    else:
        print "250 reply not received from server."

    #Informs server to quit
    socket.send("QUIT\r\n")

    #Checks server response and closes transmission channel
    msg2 = socket.recv(1024)
    if msg2[:3] == "221":
        print "221 " + server + " service closing transmission channel"
    else:
        print "221 reply not received from server."

#Server refuses recipient, terminates
elif msg[:3] == "550":
    print "550 No such user here"
    
    #Informs server to quit
    socket.send("QUIT\r\n")
    
    #Checks server response and closes transmission channel
    msg2 = socket.recv(1024)
    if msg2[:3] == "221":
        print "221 " + server + " service closing transmission channel"
    else:
        print "221 reply not received from server."

#Closes socket
socket.close()
print "Socket closed.  Have a nice a day!"
