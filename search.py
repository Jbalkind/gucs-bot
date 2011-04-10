"""
Basic web search using Yahoo.

Euan Freeman
"""

import urllib2
import json

YAHOO_API_KEY = "q4mGPszV34GhYSwsmfSUvN6VH2g_BMJtETbjnSPBC4u2sNSIQPA57mC3LbVgPvzNNyCzcBPi73kYW3d2"

def search(query, limit=5):
    url = "http://boss.yahooapis.com/ysearch/web/v1/" \
        + "{0}?appid={1}&format=json&style=raw&count={2}" \
        .format(urllib2.quote(query), YAHOO_API_KEY, limit)
    
    handle = urllib2.urlopen(url)
    
    # Decode the JSON result
    result = ""

    for line in handle:
        result += line

    handle.close()

    decoded = json.loads(result)

    return parse(decoded)

def parse(decoded):
    results = []
    
    for result in decoded[u'ysearchresponse'][u'resultset_web']:
        title = result['title']
        url = result['url']
        results += [(title, url)]
        
    return results