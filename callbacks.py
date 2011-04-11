# Callbacks
import wiki
import search
import twitter
import random
from datetime import datetime

def goofed(bot, data):
    """
    We all make mistakes
    """
    bot.send("Sorry, %s" % data["from"], channel=data["to"])

def fact(bot, data):
    """
    The "fact" motion is expressed
    """
    print data["to"]
    bot.me("slaps back of hand on opposite palm", channel = data["to"])

def wikisearch(bot, data):
    """
    Search wikipedia for a term
    """
    query = data["message"].replace("!wiki ", "")
    results = wiki.wikiSearch(query)

    if (results == []):
        bot.send("No wikipedia results for \"%s\"" % query,
                 channel = data["to"])
        return

    bot.send("Wikipedia results for \"%s\":" % query,
             channel = data["to"])

    for result in results:
        bot.send("* %s: %s" % (result[0], result[1]),
                 channel=data["to"])


def slap(bot, data):
    """
    Slap a user if they are silly
    """
    print data["to"]
    bot.me("slaps %s with a wet fish!" %data["message"].replace("!slap ", ""),
           channel = data["to"])

def sleep_time(bot,data):
    """
    Kill's the bot
    """
    bot.send("No master!! No...")
    bot.irc.quit()

def seen(bot, data):
    """
    Checks when the bot last saw a given nick
    """
    user = data["message"].replace("!seen ", "")

    if user not in bot.activity:
        bot.send("I haven't seen %s around here" % user,
                 channel = data["to"])
    else:
        lastSeen = datetime.now() - bot.activity[user]

        days = lastSeen.days
        mins = lastSeen.seconds / 60
        hours = mins / 60

        daysStr = ("%d days, " % days) if days > 0 else ""
        hoursStr = ("%d hours and " % hours) if hours > 0 else ""
        timeAgo = "%s%s%d minutes" % (daysStr, hours, mins)

        bot.send("%s was last seen %s ago" % (user, timeAgo),
                 channel = data["to"])


def moo(bot, data):
    """
    Bot sends picture of a cow
    """
    bot.send("         -__-",channel=data["to"])
    bot.send("         (oo)",channel=data["to"])
    bot.send("  /-------\/   Moooooo!",channel=data["to"])
    bot.send(" / |     ||",channel=data["to"])
    bot.send("*  ||----||",channel=data["to"])
    bot.send("   ~~    ~~",channel=data["to"])


    
def websearch(bot, data):
    """
    Search the web for a query
    """
    query = data["message"].replace("!search ", "")
    
    try:
        results = search.search(query)
    except URLError:
        bot.send("Sorry, I dun goofed",channel=data["to"])
        return
    
    if (results == []):
        bot.send("No search results for \"%s\"" % query,
                 channel=data["to"])
        return
    
    bot.send("Web results for \"%s\":" % query,channel=data["to"])
    
    for result in results:
        bot.send("* %s: %s" % (result[0], result[1]), channel=data["to"])


def twittersearch(bot, data):
    """
    Search twitter feeds for a term
    """
    query = data["message"].replace("!twitter ", "")
    
    try:
        results = twitter.search(query)
    except:
        bot.send("err... something happened, that wasn't meant to",
                 channel=data["to"])
        return

    if (results == []):
        bot.send("No twitter search results for \"%s\"" % query,
                 channel=data["to"])
        return

        bot.send("Twitter search results for \"%s\":" % query,
                 channel=data["to"])
    
    for result in results:
        bot.send("* %s: %s" % (result[0], result[1]),
                 channel=data["to"])
    

def meow(bot, data):
    """
    Bot sends a cute kitty
    """
    bot.send("  /\\_/\\", channel=data["to"])
    bot.send(" ( o.o )    meow!", channel=data["to"])
    bot.send("  > ^ <", channel=data["to"])

sventekQuotes = [
    "My momma didn't raise no fool!",
    "A baseball bat is like a cricket bat, but round.",
    "I am God. You do not change my headers!",
    "If you include a .c file, I will shoot you!",
    "I got a call from an old friend who offered me a job at a startup called Sun. I said no thanks, because I had a mortgate to pay off."
    "Heaps are the best thing since sliced bread."
]

def sventek(bot, data):
    """
    Bot delivers a line from the great man himself.
    """
    bot.send(sventekQuotes[int(random.random() * len(sventekQuotes))], channel = data["to"])

class Phrase_Response():
    """
    Class to hold information for a phrase response 
    """

    def __init__(self,  phrase, text_response):
        self.phrase = phrase
        self.text_response = text_response

    def phrase_callback(self, bot, data):
        """
        responds appropriately with registered response (response may not be appropriate)  
        """
        bot.send(self.text_response ,channel=data["to"])

def register_text_response(bot, data):
    """
    Register a text response to a given phrase
    First word is the phrase, the rest of the sentance is the text response
    for instance \t
    !register canard is cool
    has the bot respond to !canard with is cool
    """
    message = data["message"].split()
    if len(message) >= 3:
        phrase = message[1]
        response = "".join(["%s " %m for m in message[2:]])
        phrase_response = Phrase_Response(phrase, response)
        bot.register("!%s" %phrase,
                     phrase_response.phrase_callback)
        bot.send("New response registered" ,
                 channel=data["to"])
    else:
        bot.send("Could not register function" ,
                 channel=data["to"])


text_response_list = [(".*(f|F)riday.*" ,"Friday, Friday, gotta get down on Friday!"),
                                  ("((Y|y)ou have )?(p|P)roblem\?", "u mad?")]

callback_list = [("!wiki \w+", wikisearch),
                 ("!slap \w", slap),
                 ("!seen \w", seen),
                 ("!search \w+", websearch),
                 ("!twitter \w+", twittersearch),
                 ("!shutup", sleep_time),
                 ("!?(S|s)ventek!?", sventek),
                 ("(u|U) (dun|done) (goofed|goof'd|goofd)", goofed),
                 ("!register", register_text_response)
                 ]

                 # ("(m|M)eow", meow),
                 # ("(m|M)ooo*", moo),
