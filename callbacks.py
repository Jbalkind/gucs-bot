# Callbacks
import wiki
import search
import twitter
import random
import lastfm
import urllib2
import httplib
from datetime import datetime
from threading import Condition

calef_nicks = ["calef37", "scarface", "cow hoof", "cow calf", 
	       "leatherback", "The Samurai", "Colin", "sits next to Heather", "has a bit of facial hair"]
cur_boss = 0
boss_phrases = ["TALK TO CORPORATE", "APPROVE MEMOS", "LEAD A WORKSHOP",
		"REMEMBER BIRTHDAYS", "DIRECT WORKFLOW", "MY OWN BATHROOM", 
		"MICROMANAGE", "PROMOTE SYNERGY", "EAT A BAGEL", "HIT ON DEBRA",
		"GET REJECTED", "SWALLOW SADNESS", "SEND SOME FAXES",
		"CALL A SEXLINE", "CRY DEEPLY", "DEMAND A REFUND", 
		"EAT A BAGEL", "HARASSMENT LAWSUIT", "NO PROMOTION", 
		"FIFTH OF VODKA", "SHIT ON DEBRA'S DESK", "BUY A GUN",
		"IN MY MOUTH", "OH FUCK MAN CAN'T FUCKING DO IT SHIT!", 
		"PUSSY OUT", "PUKE ON DEBRA'S DESK", "JUMP OUT THE WINDOW", 
		"SUCK A DUDE'S DICK", "SCORE SOME COKE", "CRASH MY CAR", 
		"SUCK MY OWN DICK", "EAT SOME CHICKEN STRIPS", 
		"CHOP MY BALLS OFF", "BLACK OUT IN THE SEWER", 
		"MEET A GIANT FISH", "FUCK ITS BRAINS OUT", "TURN INTO A JET", 
		"BOMB THE RUSSIANS", "CRASH INTO THE SUN", "NOW I'M DEAD" ]
phrase_response_dict = {}


suggestion_mutex = Condition()
suggestion_filename = "suggestions.txt"

def suggest(bot, data):
    """
    Suggest a new feature to be added to the bot. Syntax is !suggest,
    followed by a short description of the new feature.
    """
    global suggestion_filename
    global suggestion_mutex
    message = data["message"].split()
    if len(message) >= 2:
	description = "".join(["%s "%a for a in message[1:]])
	suggestion = "Time: %s\nNick: %s\nSuggestion:\n%s\n\n"% (datetime.now().isoformat(" ") , data["from"] , description)
	#Mutex lock for writing to suggestion file
	suggestion_mutex.acquire()
	suggestion_file = open(suggestion_filename, "a")
	suggestion_file.write(suggestion)
	#Mutex has been released
	suggestion_mutex.release()
	bot.send("Thank you for your suggestion", channel=data["from"])
    else:
	bot.send("No suggestion made...", channel=data["from"])

def calefnick(bot, data):
    """
    Calum has a lot of nicknames
    """
    random.seed()
    bot.send("%s" % calef_nicks[random.randint(0,len(calef_nicks)-1)], 
	     channel=data["to"])

def boss_rand(bot, data):
    """
    Spit out a random lyric from 'like a boss'
    """
    random.seed()
    bot.send("%s" % boss_phrases[random.randint(0, len(boss_phrases)-1)], channel=data["to"])

def boss_ord(bot, data):
    """
    Spits out the lyrics from 'like a boss' in order, uses a global
    variable to keep track
    """
    global cur_boss
    if(cur_boss == len(boss_phrases)-1):
	cur_boss = 0;

    bot.send("%s" % boss_phrases[cur_boss], channel=data["to"])
    cur_boss += 1


def goofed(bot, data):
    """
    We all make mistakes
    """
    bot.send("Sorry, %s" % data["from"], channel=data["to"])
    

def wikisearch(bot, data):
    """
    Search wikipedia for a term. @sends result to channel, !sends
    result in a personal message
    """
    if data["message"][0] == "!":
	query = data["message"].replace("!wiki ", "")
	destination = "from"
    else: 
	query = data["message"].replace("@wiki ", "")
	destination = "to"
    
    results = wiki.wikiSearch(query)

    if (results == []):
	bot.send("No wikipedia results for \"%s\"" % query,
		 channel = data[destination])
	return

    bot.send("Wikipedia results for \"%s\":" % query,
	     channel = data[destination])

    for result in results:
	bot.send("* %s: %s" % (result[0], result[1]),
		 channel=data[destination])


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
    bot.send("	       -__-",channel=data["to"])
    bot.send("	       (oo)",channel=data["to"])
    bot.send("	/-------\/   Moooooo!",channel=data["to"])
    bot.send(" / |     ||",channel=data["to"])
    bot.send("*	 ||----||",channel=data["to"])
    bot.send("	 ~~    ~~",channel=data["to"])


    
def websearch(bot, data):
    """
    Search the web for a query. use @ to send result to channel, and ! to receive as personal message
    """
    if data["message"][0] == "!":
	query = data["message"].replace("!search ", "")
	destination = "from"
    else: 
	query = data["message"].replace("@search ", "")
	destination = "to"
    
    try:
	results = search.search(query)
    except URLError:
	bot.send("Sorry, I dun goofed",channel=data[destination])
	return
    
    if (results == []):
	bot.send("No search results for \"%s\"" % query,
		 channel=data[destination])
	return
    
    bot.send("Web results for \"%s\":" % query,channel=data[destination])
    
    for result in results:
	bot.send("* %s: %s" % (result[0], result[1]), channel=data[destination])


def twittersearch(bot, data):
    """
    Search twitter feeds for a term
    """
    if data["message"][0] == "!":
	query = data["message"].replace("!twitter ", "")
	destination = "from"
    else: 
	query = data["message"].replace("@twitter ", "")
	destination = "to"
    
    try:
	results = twitter.search(query)
    except:
	bot.send("err... something happened, that wasn't meant to",
		 channel=data[destination])
	return

    if (results == []):
	bot.send("No twitter search results for \"%s\"" % query,
		 channel=data[destination])
	return

	bot.send("Twitter search results for \"%s\":" % query,
		 channel=data["to"])
    
    for result in results:
	bot.send(u"* %s: %s" % (result[0], result[1]),
		 channel=data["to"])
    

def meow(bot, data):
    """
    Bot sends a cute kitty
    """
    bot.send("	/\\_/\\", channel=data["to"])
    bot.send(" ( o.o )	  meow!", channel=data["to"])
    bot.send("	> ^ <", channel=data["to"])

sventekQuotes = [
    "My momma didn't raise no fool!",
    "A baseball bat is like a cricket bat, but round.",
    "I am God. You do not change my headers!",
    "If you include a .c file, I will shoot you!",
    "I got a call from an old friend who offered me a job at a startup called Sun. I said no thanks, because I had a mortgate to pay off.",
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

    def __init__(self,	phrase, text_response):
	self.phrase = phrase
	self.text_response = text_response

    def phrase_callback(self, bot, data):
	"""
	responds appropriately with registered response (response may not be appropriate)  
	"""
	bot.send(self.text_response ,channel=data["to"])

def unregister_text_response(bot,data):
    """
    Unregister a text response to a phrase, syntax \t
    !unregister phrase
    """
    global phrase_response_dict
    message = data["message"].split()
    if len(message) >=2:
	phrase = message[1]
	if phrase in phrase_response_dict:
	    phrase_response = phrase_response_dict.pop(phrase)
	    bot.unregister("!%s"%phrase)
	    
def register_text_response(bot, data):
    """
    Register a text response to a given phrase
    First word is the phrase, the rest of the sentance is the text response
    for instance \t
    !register canard is cool
    has the bot respond to !canard with is cool
    """
    global phrase_response_dict
    message = data["message"].split()
    if len(message) >= 3:
	phrase = message[1]
	response = "".join(["%s " %m for m in message[2:]])
	phrase_response = Phrase_Response(phrase, response)
	bot.register("!%s" %phrase,
		     phrase_response.phrase_callback)
	phrase_response_dict[phrase] = phrase_response
	bot.send("New response registered" ,
		 channel=data["to"])
    else:
	bot.send("Could not register function" ,
		 channel=data["to"])

def fact(bot, data):
    bot.me("smacks back of hand on palm of other hand in approval.", data["to"])

def last(bot, data):
    """
    Returns the song last.fm <user> is currently playing 
    """
    
    user = data["message"].replace("!last ","")
    
    playing = lastfm.nowplaying(user)

    if playing == []:
	bot.send("No result found", data["to"])
    else:
	for result in playing:
	    bot.send("" + user + " is Now Playing: " + 
		     result[0] + " - " + result[1] + "", data["to"])

def similar_artists(bot,data):
    """
    Returns similar artists to specified artist using last.fm's suggestions
    """
    
    artist = data["message"].replace("!similar ", "")
    
    similar = lastfm.getsimilar(artist)
    
    if similar == []:
	bot.send("No results found", data["to"])
    else:
	results = ""
	for result in similar:
	    results += result + ", "
	    
	bot.send("Similar artists: " + results, data["to"])


def findtitle(bot, data):
    # Returns the title of a website
    url = data["message"]
    
    url = url.replace("http://","")
    
    if "/" in url:
	i = url.index("/")
	therest = url[i:len(url)]
	url =url[0:i]
    else:
	url = url
	therest = ""

    conn = httplib.HTTPConnection(url)
    conn.request("HEAD", therest)
    res = conn.getresponse()

    for headers in res.getheaders():
	if headers[0] == "content-type" and 'text/html' in headers[1]:
	    try: 
		url = data["message"]
		
		results = []
		   
		handle = urllib2.urlopen(url)
		
		title = ""
		result = ""
	    
		for line in handle:
		    result += line
	    
		handle.close()
	    
		if '<title>' in result and '</title>' in result:
		    temp = result.split('<title>')[1]
		    title = temp.split('</title>')[0]
		    bot.send(title.replace("\n", ""), data["to"])
	    
	    
	    except:
		print "This site either doesn't exist, or doesn't appreciate urllib"
    

#This list stores patterns and an associated text response. These are
#loaded by the bot on startup or on !update
text_response_list = [(".*(f|F)riday.*" ,"Friday, Friday, gotta get down on Friday!"), ("((Y|y)ou have )?(p|P)roblem\?", "u mad?"), (".*(w|W)hat is bulk type?.*", "12.45"),
		      (".*(a|A)mirite?.*", "urrite!")]

callback_list = [("(!|@)wiki \w+", wikisearch),
		 ("!slap \w", slap),
		 ("!seen \w", seen),
		 ("(!|@)search \w+", websearch),
		 ("(!|@)twitter \w+", twittersearch),
		 ("!shutup", sleep_time),
		 ("!?(S|s)ventek!?", sventek),
		 ("(u|U) (dun|done) (goofed|goof'd|goofd)", goofed),
		 ("!register", register_text_response),
	   	 ("!unregister",unregister_text_response),
		 (".*(f|F)act.*", fact),
		 ("!last \w", last),
		 ("!similar \w+", similar_artists),
		 ("http://\w", findtitle),
		 (".*calef13\.randnick\(\).*", calefnick),
		 (".*LIKE A BOSS.*", boss_rand),
		 (".*like a boss.*", boss_ord),
		 ("!suggest", suggest)]

