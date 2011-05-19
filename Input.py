import threading
 
class Input(threading.Thread):
    """ Handle input from the server """
    
    def __init__(self, irc):
        threading.Thread.__init__(self)
        self.irc = irc
        self.owners = ["Happy0", "canard", "JamesMc", "Euan", "Finde", "heather_hb","calef13", "CMCL"]
        self.observers = []
        
    def privmsg(self, data, raw = None):
	"""Handles an privmsg commands."""
	# Split up channel name and message content
        parts = data["message"].split(" ", 1)
	# Channel name is the "to" entry in the data dictionary
        data["to"] = parts[0]
	# Chop off the : and any padding
        data["message"] = parts[1].split(":", 1)[1].strip()
        
	# Only owners can close the bot connection
        if data["from"] in self.owners and data["message"] == "gucs-bot.quit()":
            self.irc.quit()
        
        if data["CTCP"]:
            print " " * 17 + "* {} {}".format(data["from"], data["message"])
        else:
            print "{:18} | {}".format(data["from"], data["message"])
            
            for observer in self.observers:
                observer.notify(data)
        
        
    def run(self):
	"""Attach the callback functions to the commands and run the parser."""
        self.irc.attach("PRIVMSG", self.privmsg)
   
        for line in self.irc.incoming():
            pass
                
    def registerObserver(self, observer):
        self.observers += [observer]
