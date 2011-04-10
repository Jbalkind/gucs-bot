# Callbacks

import wiki
import search
import twitter
from datetime import datetime

def umad(bot, data):
    bot.send("U mad?",)


def friday(bot, data):
    bot.send("Friday, friday, gotta get down on Friday!", channel=data["to"])


def goofed(bot, data):
    bot.send("Sorry, %s" % data["from"], channel=data["to"])


def wikisearch(bot, data):
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
    print data["to"]
    bot.me("slaps %s with a wet fish!" %data["message"].replace("!slap ", ""),
           channel = data["to"])

def sleep_time(bot,data):
    bot.send("No master!! No...")
    bot.irc.quit()

def seen(bot, data):
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
    bot.send("         -__-",channel=data["to"])
    bot.send("         (oo)",channel=data["to"])
    bot.send("  /-------\/   Moooooo!",channel=data["to"])
    bot.send(" / |     ||",channel=data["to"])
    bot.send("*  ||----||",channel=data["to"])
    bot.send("   ~~    ~~",channel=data["to"])
    
def websearch(bot, data):
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

        
callback_list = [("(p|P)roblem\?", umad),
                 ("(f|F)riday", friday),
                 ("(u|U) (dun|done) (goofed|goof'd|goofd)", goofed),
                 ("!wiki \w+", wikisearch),
                 ("!slap \w", slap),
                 ("!seen \w", seen),
                 ("(m|M)ooo*", moo),
                 ("!search \w+", websearch),
                 ("!twitter \w+", twittersearch)]


