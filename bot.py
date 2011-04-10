import threading
import Input
import Output
from Irc.irc import Irc
from datetime import datetime
import re # Regular expressions
import wiki
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


def slap(bot, data):
    bot.me("slaps %s with a wet fish!" % data["message"].replace("!slap ", ""))


def seen(bot, data):
    user = data["message"].replace("!seen ", "")

    if user not in bot.activity:
        bot.send("I haven't seen %s around here" % user)
    else:
        lastSeen = datetime.now() - bot.activity[user]

        days = lastSeen.days
        mins = lastSeen.seconds / 60
        hours = mins / 60

        daysStr = ("%d days, " % days) if days > 0 else ""
        hoursStr = ("%d hours and " % hours) if hours > 0 else ""
        timeAgo = "%s%s%d minutes" % (daysStr, hours, mins)

        bot.send("%s was last seen %s ago" % (user, timeAgo))


def moo(bot, data):
    bot.send("         (__)")
    bot.send("         (oo)")
    bot.send("  /-------\/   Moooooo!")
    bot.send(" / |     ||")
    bot.send("*  ||----||")
    bot.send("   ~~    ~~")

def update(bot, data):
    if (data["from"] in bot.input.owners):
        os.spawnv(os.P_NOWAIT, update.sh, [])
        self.irc.quit()






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
    gucsbot.register("!slap \w", slap)
    gucsbot.register("!seen \w", seen)
    gucsbot.register("(m|M)ooo*", moo)
    gucsbot.register("!update", update)

if __name__ == "__main__":
    main()