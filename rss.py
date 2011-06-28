# Created on 27/6/2011 by Craig McL
# Purpose : RSS reader

import xml.dom.minidom
import urllib2

class RSSReader(object):
    FILENAME = "feeds.txt"
    def __init__(self):
        """Loads in feeds from file if given.

        File format must be each line:
        feedName:feedURL
        """
        # Dicitionary holds command (feedName) and feed url pairs
        self.feeds = {}
        try:
            with open(RSSReader.FILENAME, 'r') as f:
                for line in f:
                    line = line.strip()
                    cmd, feed = line.split(":", 1)
                    self.feeds[cmd] = feed
        except IOError as inst:
            print "File {} doesn't exist!(RSSReader)".format(RSSReader.FILENAME)

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

    def get_url(self, urlStr):
        """Returns a file-like object to the URL specified by urlStr."""
        request = urllib2.Request(urlStr)
        # Change header to spoof our User-Agent
        request.add_header("User-Agent", "Mozilla/5.0")
        source = urllib2.urlopen(request)
        return source

    def get_xml_document(self, urlStr):
        """Returns the document object of a URL."""
        # Return our Document object
        dom = xml.dom.minidom.parse(self.get_url(urlStr))
        return dom

    def get_feed(self, bot, data, feed):
        if self.feeds.get(feed, None):
            feedURL = self.feeds[feed]
            dom = self.get_xml_document(feedURL)
            # Get feed titles
            titles = dom.getElementsByTagName("title")
            links = dom.getElementsByTagName("link")
            # Send titles and corresponding links
            for i in xrange(6):
                bot.send(self.get_feed_data(
                    titles[i].childNodes, links[i].childNodes), data["from"])
        else:
            bot.send("Not subscribed to feed.", data["from"])

    def add_feed(self, bot, data, feedName, feedURL):
        if ":" not in feedName:
            self.feeds[feedName] = feedURL
            bot.send("Subscribed to feed.", data["from"])
        else:
            bot.send("Cannot have ':' in feed name.", data["from"])
        
    def del_feed(self, bot, data, feedName):
        result = self.feeds.pop(feedName, None)
        msg = ""
        if result is not None:
            msg = "Feed for {} removed.".format(feedName)
        else:
            msg = "Not subscribed to feed {}".format(feedName)
        bot.send(msg, data["from"])

    def save_feeds(self):
        """Saves the feeds to file."""
        try:
            with open(RSSReader.FILENAME, 'w') as f:
                for feedName, feedURL in self.feeds.items():
                    line = "{}:{}\n".format(feedName, feedURL)
                    f.write(line)
            print "Feeds saved to file. (RSSReader)"
        except IOError as inst:
            print "Error occurred when writing to file {}. (RSSReader)".format(
                RSSReader.FILENAME)
                
