# Author: Happy0
# Does things with various calls to the last.fm API :P

from xml.dom import minidom
import urllib2
import urllib

def nowplaying(user):
    # Returns what the user is currently playing (if anything)

    try:
        api_key = open('lastapi.txt', 'r').read()
    except:
        print "lastapi.txt file doesn't exit"
        return []
        
    url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=%s&limit=1&api_key=%s" %(user, api_key)
    results = []
          
    try:    
        dom = getresults(url)
  
        for result in dom.getElementsByTagName("track"):
            if (result.hasAttributes()): # There is a "now playing" attribute, if they're currently playing a song
                
                artist = result.getElementsByTagName("artist")[0].childNodes[0].nodeValue.encode(encoding='utf8')
                title = result.getElementsByTagName("name")[0].childNodes[0].nodeValue.encode(encoding='utf8')
            
                results += [(artist, title)]
            
    except:
        print "bad url"
    
    return results


def getsimilar(artist):
    # Returns similar artists, to a given artist
    
    try:
        api_key = open('lastapi.txt', 'r').read()
    except:
        print "lastapi.txt file doesn't exit"
        return []
        
    url = "http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist=%s&limit=10&api_key=%s" %(urllib2.quote(artist),api_key)
    results = []
    
    try:    
        dom = getresults(url)
        for result in dom.getElementsByTagName("artist"):
            artist = result.getElementsByTagName("name")[0].childNodes[0].nodeValue
            results += [(artist)]    
    except:
        print "bad url"
    
    return results
    
     
    

def getresults(url):
    handle = urllib2.urlopen(url)
    result = ""

    for line in handle:
        result += line

    handle.close()

    return minidom.parseString(result)
    
    


def main():
    results= getsimilar("A Sunny Day In Glasgow")

    for result in results:
        print result


if __name__ == "__main__":
    main()
    
