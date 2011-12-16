# Author: Happy0
# Does things with the dictionary.com API :P

from xml.dom import minidom
import urllib2
import urllib

def define(word):
    results = []
    
    try:
        api_key = open('dictapi.txt', 'r').read()
    except:
        print "dictapi.txt file doesn't exit"
        return []
    
    url = "http://api-pub.dictionary.com/v001?vid={}&q={}&type=define".format(
        api_key, word)
    
    try:
        dom = getresults(url) 
        
        for result in dom.getElementsByTagName("defset"):
            results += [result.getElementsByTagName("def")[0].childNodes[0].nodeValue]
                
            
        return results 
    except:
        print "bad url"
        return []


def getresults(url):
    
    handle = urllib2.urlopen(url)
    result = ""

    for line in handle:
        result += line

    handle.close()

    return minidom.parseString(result)



def main():
   results = define("hello")
   
   if results != []:
       for result in results:
           print result


if __name__ == "__main__":
    main()
