import threading
 
class Input(threading.Thread):
    """ Handle input from the server """
    
    def __init__(self, irc):
        threading.Thread.__init__(self)
        self.irc = irc
        self.owners = ["JamesMc", "euan", "Happy0", "Finde"]
        self.observers = []
        
    """ Handles an privmsg commands """
    def privmsg(self, data, raw = None):
        parts = data["message"].split(" ", 1)
        data["to"] = parts[0]
        data["message"] = parts[1].split(":", 1)[1].strip() # Chop off the : and any padding
        
        if data["from"] in self.owners and data["message"] == "gucs-bot.quit()":
            self.irc.quit()
        
        if data["CTCP"]:
            print " " * 17  + "* %s %s" % (data["from"], data["message"])
        else:
            print "%18s | %s" % (data["from"], data["message"])
            
            for observer in self.observers:
                observer.notify(data)
        
        
    """ Attach the callback functions to the commands and run the parser """
    def run(self):
        self.irc.attach("PRIVMSG", self.privmsg)
   
        for line in self.irc.incoming():
            pass
                
    def registerObserver(self, observer):
        self.observers += [observer]