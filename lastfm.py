# Author: Gordon Martin
# Does things with various calls to the last.fm API :P

from xml.dom import minidom
import urllib2
import urllib

def nowplaying(user):
    # Returns what the user is currently playing (if anything)

    try:
        api_key = open('lastapi.txt', 'r').read()
    except:
        print "file doesn't exit"

        
    url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=%s&limit=1&api_key=%s" %(user, api_key)

    
    handle = urllib2.urlopen(url)

    result = ""

    for line in handle:
        result += line

    handle.close()

    dom = minidom.parseString(result)

    results = []
    
    for result in dom.getElementsByTagName("track"):
        if (result.hasAttributes()): # There is a "now playing" attribute, if they're currently playing a song
            
            artist = result.getElementsByTagName("artist")[0].childNodes[0].nodeValue
            title = result.getElementsByTagName("name")[0].childNodes[0].nodeValue
        
            results += [(artist, title)]
    
    return results



def main():
    results= nowplaying("Happy0")

    for result in results:
        print result[0], result[1]


if __name__ == "__main__":
    main()
    
