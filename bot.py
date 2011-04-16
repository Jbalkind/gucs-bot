#!/usr/bin/python
import threading
import Input
import Output
import callbacks
from callbacks import Phrase_Response
from Irc.irc import Irc
from datetime import datetime
import re
import os
import argparse

class Observer:
    def notify(self, msg):
        pass

class Bot(Observer):
    """
    Simple IRC bot.

    Respond to chatter by registering callbacks which
    are triggered by a regular expression pattern match.
    """

    def __init__(self, server, channels, nick, name):
        self.nick = nick
        
        self.irc = Irc()
        self.irc.connect(server)
        self.irc.set_info(nick, nick)

        self.channels = channels

        for channel in channels:
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
                
                # This makes the bot respond directly to personal messages
                if data["to"] == self.nick:
                    data["to"] = data["from"]
                
                self.callbacks[pattern](self, data)
                break

        self.activity[data["from"]] = datetime.now()


    def register(self, pattern, callback):
        """
        Registers a callback for an input pattern.
        """
        self.callbacks[pattern] = callback
        
    def unregister(self, pattern):
        """
        Unregister a function
        """
        self.callbacks.pop(pattern)

    def send(self, msg, channel=""):
        """
        Sends a message to specified channel.
        """
        #if channel == "": channel = self.channel

        self.irc.send(channel, msg)


    def me(self, msg, channel=""):
        """
        Sends a /me message to specified channel.
        """
        #if channel == "": channel = self.channel

        self.irc.me(channel, msg)

def force_reload(bot,data):
    """
    Force the bot to reload its callback methods
    """
    if (data["from"] in bot.input.owners):
    	try:
            reload(callbacks)
            load_callbacks(bot)
            bot.send("Callbacks reloaded", channel = data["from"])
    	except:
    		bot.send("There was an error in callbacks.py, callbacks were not reloaded.", channel = data["from"])


def help_user(bot, data):
    """
    Help function for the bot
    """
    bot.send("List of functions that this bot makes availible;",
             channel=data["from"])
    for callback, function in bot.callbacks.items():
        #Change newlines to spaces
        if function.__doc__ == None:
            help_string = "No help for this function"
        else:
            help_string = function.__doc__.replace('\n'," ") 
        bot.send("%s \t- %s" %(callback, help_string.strip()),
                 channel=data["from"])

def load_callbacks(bot):
    """
    Reload the callbacks for this bot
    """
    for name, function in callbacks.callback_list:
        bot.register(name, function)
    for phrase, response in callbacks.text_response_list:
        phrase_response = Phrase_Response(phrase, response)
        bot.register(phrase, phrase_response.phrase_callback)

def svn_update(bot, data):
    """
    Update this bot with code from the svn repository
    """
    if (data["from"] in bot.input.owners):
        os.system("svn update")
        bot.send("SVN updated", channel = data["from"])
        force_reload(bot,data)


# Main function
def main(server, nick, channels, name):
    gucsbot = Bot(server, channels, nick, name)
    load_callbacks(gucsbot)
    gucsbot.register("!update", force_reload)
    gucsbot.register("!help", help_user)
    gucsbot.register("!svn", svn_update)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Friendly, Python, IRC bot")
    parser.add_argument("-s","--server",dest="server",action="store",
                        default="irc.freenode.net",
                        help="Name of IRC server to connect to, default is freenode")
    parser.add_argument("-n","--nick",dest="nick",action="store",
                        default="gucs_bot",
                        help="Nickname for bot")
    parser.add_argument("--name",dest="name",action="store",
                        default="gucs_bot",
                        help="Name of bot")
    parser.add_argument("channels", type = str, metavar='C',
                        help="Channels to connect to, include \#'s with quotation marks",
                        nargs='+',)
    args = parser.parse_args()
    main(server = args.server, nick = args.nick, name = args.name,
         channels = args.channels)

