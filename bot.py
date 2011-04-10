import threading
import Input
import Output 
from Irc.irc import Irc
import re # Regular expressions
import wiki

class Observer:
    def notify(self, msg):
        pass

class Bot(Observer):
    """
    Simple IRC bot.
    
    Respond to chatter by registering callbacks which
    are triggered by a regular expression pattern match.
    """
    
    def __init__(self, server, channel, nick, name):
        self.irc = Irc()
        self.irc.connect(server)
        self.irc.set_info(nick, nick)
        
        self.channel = channel
        
        self.irc.join(channel)
        self.irc.me(channel, "has initiated self-destruct sequence!")
    
        self.input = Input.Input(self.irc)
        self.input.registerObserver(self)
        self.input.start()
        
        self.output = Output.Output(self.irc)
        self.output.start()
        
        self.callbacks = {}
    
    
    def notify(self, data):
        """
        Respond to notification that some event being
        observed has occurred.
        
        Compares the given message against a collection
        of patterns and executes any appropriate callbacks.
        
        * data = {"from", "to", "message"}
        """
        for pattern in self.callbacks.keys():
            if re.match(pattern, data["message"]) != None:
                self.callbacks[pattern](self, data)
                break
                
    
    def register(self, pattern, callback):
        """
        Registers a callback for an input pattern.
        """
        self.callbacks[pattern] = callback
    
    
    def send(self, msg, channel=""):
        """
        Sends a message to specified channel.
        """
        if channel == "": channel = self.channel
        
        self.irc.send(channel, msg)
    
    
# Callbacks
def umad(bot, data):
    bot.send("U mad?")


def friday(bot, data):
    bot.send("Friday, friday, gotta get down on Friday!")
    

def goofed(bot, data):
    bot.send("Sorry, %s" % data["from"])


def wikisearch(bot, data):
    query = data["message"].replace("!wiki ", "")
    results = wiki.wikiSearch(query)
    
    if (results == []):
        bot.send("No wikipedia results for \"%s\"" % query)
        return
    
    bot.send("Wikipedia results for \"%s\":" % query)
    
    for result in results:
        bot.send("* %s: %s" % (result[0], result[1]))


# Main function
def main():
    server = "irc.freenode.net"
    nick = "gucs-bot"
    channel = "##GUCS"
    name = "Sir Trollface Esq."
    
    gucsbot = Bot(server, channel, nick, name)
    
    # Register callbacks to give gucs-bot something to do
    gucsbot.register("(p|P)roblem\?", umad)
    gucsbot.register("(f|F)riday", friday)
    gucsbot.register("(u|U) (dun|done) (goofed|goof'd|goofd)", goofed)
    gucsbot.register("!wiki \w+", wikisearch)
    
if __name__ == "__main__":
    main()