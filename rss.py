# Created on 27/6/2011 by Craig McL
# Purpose : XHTML/XML(RSS) reader

import xml.dom.minidom
import urllib2

class DOMReader(object):
    FILENAME = "feeds.txt"
    def __init__(self):
        """Loads in feeds from file if given.

        File format must be each line:
        feedName:feedURL"""
        # Dicitionary holds command (feedName) and feed url pairs
        self.feeds = {}
        try:
            with open(DOMReader.FILENAME, 'r') as f:
                for line in f:
                    line = line.strip()
                    cmd, feed = line.split(":")
                    self.feeds[cmd] = feed
        except IOError as inst:
            pass

    def get_feed_data(self, titleList, linkList):
        """Returns a string with both the title and link specified by args."""
        title = self.get_text(titleList)
        link = self.get_text(linkList)
        return "{} -> {}".format(title, link)

    def get_text(self, nodeList):
        """Return the text from the given nodelist object."""
        text = []
        for node in nodeList:
            if node.nodeType == node.TEXT_NODE:
                # Append to text node getting rid of any newlines
                text.append(node.nodeValue.strip())
        return " ".join(text)

    def get_document(self, urlStr):
        """Returns the document object of a URL."""
        request = urllib2.Request(urlStr)
        # Change header to spoof our User-Agent
        request.add_header("User-Agent", "Mozilla/5.0")
        source = urllib2.urlopen(request)
        # Return our Document object
        return xml.dom.minidom.parse(source)

    def get_feed(self, bot, data, feed):
        if self.feeds.get(feed, None):
            feedURL = self.feeds[feed]
            dom = self.get_document(feedURL)
            # Get feed titles
            titles = dom.getElementsByTagName("title")
            links = dom.getElementsByTagName("link")
            # Send titles and corresponding links
            for i in xrange(6):
                bot.send(self.get_feed_data(
                    titles[i].childNodes, links[i].childNodes), data["from"])
        else:
            bot.send("Not subscribed to feed.", data["from"])

            
                
