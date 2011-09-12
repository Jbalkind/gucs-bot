import socket
import binascii
from time import sleep
import string

class Irc:
    """ A simple class for basic IRC access """
    
    _hex01 = binascii.unhexlify("01")
    callback = {}
    
    def __init__(self):
        self.socket = socket.socket()
      
    
    def connect(self, server, port = 6667):
	"""Attempt to connect to the specifed server on the given port."""
        self.server = server
        self.socket.connect((server, port))
        
    
    def set_info(self, nickname, realname):
	"""Set the users information on the server. 

	This must be called after connect() and before any other command.
	"""
        if not self.server:
            raise NotConnected
        
        self.nickname = nickname
        self.realname = realname
        
        self.socket.send("NICK {}\r\n".format(nickname))
        self.socket.send("USER {} {} {} :{}\r\n".format(nickname, self.server, self.server, realname))
        
        
    def password(self, password):
	"""Send the password to identify the user."""
        self.socket.send("PRIVMSG NickServ :identify {}\r\n".format(password))
        
        
    
    def join(self, room):
	"""Attempt to join the specified room(s). 

	Seperate multiple rooms with a single comma and no space (e.g., 
        #chan1,#chan2).
	"""
        if not self.nickname:
            raise NoInfoSet
        
        self.socket.send("JOIN :{}\r\n".format(room))
        
    
    def send(self, channel, msg):
        """Sends a message to the channel(s).

	Message is separated by a single
        comma and no spaces.
        """
        if not self.nickname:
            raise NoInfoSet

        try:
            for line in string.split(msg,'\n'):
                print line
                sleep(1)
                self.socket.send(u"PRIVMSG {} :{}\r\n".format(channel, line))
        except:
            self.socket.send(u"PRIVMSG {} :{}\r\n".format(channel, "[an exception was raised]"))
         
    def me(self, channel, msg):
	"""Send a /me command to the specifed room."""
        if not self.nickname:
            raise NoInfoSet
            
        self.socket.send("PRIVMSG {} :{}ACTION {}{}\r\n".format(channel, self._hex01, msg, self._hex01))
            
         
         
    def parse(self, line):
	"""Parse a line sent by the server.

	Pass it to any callback commands that have been registered for it.
	"""
	# Store message information in a dictionary
        data = {}
        parts = line.split(":", 1)

        if len(parts) > 1:
            # Split sender info, command, channel with message into
	    # separate list elements.
            parts = parts[1].split(" ", 2)
	    # Split up senders nick and host
            info = parts[0].split("!", 1)

            if len(info) > 1:
                data["from"] = info[0]
                data["host"] = info[1]
            
            if len(parts) > 2:
		# message is both channel name and message separated by a colon.
                data["message"] = parts[2]
                data["CTCP"] = (data["message"][0] == self._hex01 and data["message"][-1] == self._hex01)

            if len(parts) > 1:
                data["command"] = parts[1]
                
                # Call the callback functions
                for func in self.callback.get(data["command"], []):
                    func(data, line)
                    
                if not self.callback.get(data["command"], []):
                    print "No callback registered for {}:\n{}".format(data["command"], line.strip())
            
    
    def attach(self, cmd, function):
	"""Register a function to be called when a command is recieved."""
        self.callback[cmd] = self.callback.get(cmd, [])
        self.callback[cmd] += [function]
        
            
    def incoming(self):
	"""Yield the incoming data to the caller. 

	This handles any PING commands.
	"""
        if not self.server:
            raise NotConnected
            
        while True:
            try:
                lines = self.socket.recv(1024)
            except socket.error, e:
                if e.args[0] == socket.EBADF:
                    print "Err: Bad file descriptor!"
                    exit(1)
                      
            # Make sure we've not closed the socket
            if not lines:
                break
                
            for line in lines.split("\n"):
                parts = line.split(":", 1)
                if parts[0].find("PING") != -1:
                    self.socket.send("PONG :{}".format(parts[1]))
                    continue
                    
                self.parse(line)
                yield line
            
            
    def quit(self):
	"""Quit IRC."""
        self.socket.close()
            
class Error(Exception):
    pass
    
    
class NotConnected(Error):
    pass
    
    
class NoInfoSet(Error):
    pass
