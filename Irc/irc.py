import socket
import binascii

class Irc:
    """ A simple class for basic IRC access """
    
    _hex01 = binascii.unhexlify("01")
    callback = {}
    
    def __init__(self):
        self.socket = socket.socket()
      
    
    """ Attempt to connect to the specifed server on the given port """
    def connect(self, server, port = 6667):
        self.server = server
        self.socket.connect((server, port))
        
    
    """ Set the users information on the server. This must be called after connect() and before any other command """
    def set_info(self, nickname, realname):
        if not self.server:
            raise NotConnected
        
        self.nickname = nickname
        self.realname = realname
        
        self.socket.send("NICK %s\r\n" % (nickname))
        self.socket.send("USER %s %s %s :%s\r\n" % (nickname, self.server, self.server, realname))
        
        
    """ Send the password to identify the user """  
    def password(self, password):
        self.socket.send("PRIVMSG NickServ :identify %s\r\n" % (password))
        
        
    """ Attempt to join the specified room(s). Seperate multiple rooms with a single comma and no space (e.g., 
        #chan1,#chan2) """
    def join(self, room):
        if not self.nickname:
            raise NoInfoSet
        
        self.socket.send("JOIN :%s\r\n" % (room))
        
    
    def send(self, channel, msg):
        """
        Sends a message to the channel(s), separated by a single
        comma and no spaces.
        """
        if not self.nickname:
            raise NoInfoSet
            
        self.socket.send("PRIVMSG %s :%s\r\n" % (channel, msg))
        
        
    """ Send a /me command to the specifed room """ 
    def me(self, channel, msg):
        if not self.nickname:
            raise NoInfoSet
            
        self.socket.send(u"PRIVMSG %s :%sACTION %s%s\r\n" % (channel, self._hex01, msg, self._hex01))
            
         
    """ Parse a line sent by the server and pass it to any callback commands that have been registered for it """     
    def parse(self, line):
        data = {}   
        parts = line.split(":", 1)
        
        if len(parts) > 1:
            parts = parts[1].split(" ", 2)
            info = parts[0].split("!", 1)

            if len(info) > 1:
                data["from"] = info[0]
                data["host"] = info[1]
            
            if len(parts) > 2:
                data["message"] = parts[2]
                data["CTCP"] = (data["message"][0] == self._hex01 and data["message"][-1] == self._hex01)

            if len(parts) > 1:
                data["command"] = parts[1]
                
                # Call the callback functions
                for func in self.callback.get(data["command"], []):
                    func(data, line)
                    
                if not self.callback.get(data["command"], []):
                    print "No callback registered for %s:\n%s" % (data["command"], line.strip())
            
          
    """ Register a function to be called when a command is recieved """
    def attach(self, cmd, function):
        self.callback[cmd] = self.callback.get(cmd, [])
        self.callback[cmd] += [function]
        
         
    """ Yield the incoming data to the caller. This handles any PING commands. """   
    def incoming(self):
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
                    self.socket.send("PONG :%s" % (parts[1]))
                    continue
                    
                self.parse(line)
                yield line
            
     
    """ Quit IRC """       
    def quit(self):
        self.socket.close()
            
class Error(Exception):
    pass
    
    
class NotConnected(Error):
    pass
    
    
class NoInfoSet(Error):
    pass
