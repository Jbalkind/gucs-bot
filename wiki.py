"""
Basic wikipedia search script.

Searches for a given phrase then parses
the XML result obtained.

Euan Freeman
"""

from xml.dom import minidom
import urllib2

def wikiSearch(query, limit=5):
    """
    Performs a basic wikipedia search and parses
    the document object model obtained for the results.
    
    * query := Phrase to search for
    * limit := Maximum number of results
    """
    url = "http://en.wikipedia.org/w/api.php?" \
        + "format=xml&action=opensearch&limit=%d&search=%s" \
        % (limit, urllib2.quote(query))
        
    handle = urllib2.urlopen(url)
    
    # Decode the JSON result
    result = ""

    for line in handle:
        result += line

    handle.close()

    dom = minidom.parseString(result)
    
    return parse(dom)

def parse(dom):
    """
    Parses the document object model for some wikipedia
    search results, returning a list of tuples in the
    following format:
        [(title, url), (title, url), ...]
        
    * dom := Document object model for results
    """
    results = []
    
    for result in dom.getElementsByTagName("Item"):
        title = result.getElementsByTagName("Text")[0].childNodes[0].nodeValue
        url = result.getElementsByTagName("Url")[0].childNodes[0].nodeValue
        
        results += [(title, url)]
        
    return results