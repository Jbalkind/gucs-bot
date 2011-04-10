import threading
import Input
import Output
import callbacks
from Irc.irc import Irc
from datetime import datetime
import re
import os

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
        self.activity = {} # Maps usernames to activity


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

        self.activity[data["from"]] = datetime.now()


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


    def me(self, msg, channel=""):
        """
        Sends a /me message to specified channel.
        """
        if channel == "": channel = self.channel

        self.irc.me(channel, msg)

def force_reload(bot,data):

	try:
		reload(callbacks)
		load_callbacks(bot)
	except:
		bot.send("There was an error in callbacks.py, callbacks were not reloaded.")



def load_callbacks(bot):
    for callback_tuple in callbacks.callback_list:
        bot.register(callback_tuple[0], callback_tuple[1])

def svn_update(bot, data):
	os.system("svn update")


# Main function
def main():
    server = "irc.freenode.net"
    nick = "gucsbot"
    channel = "##GUCS"
    name = "Sir Trollface Esq."

    gucsbot = Bot(server, channel, nick, name)
    load_callbacks(gucsbot)
    gucsbot.register("!update", force_reload)
    gucsbot.register("!svn", svn_update)

if __name__ == "__main__":
    main()
