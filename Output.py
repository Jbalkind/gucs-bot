import threading   
from threading import Timer     
from time import sleep
        
class Output(threading.Thread):
    """ Generate output for the server at "random" times """
    
    def __init__(self, irc):
        threading.Thread.__init__(self)
        self.irc = irc
        
    def run(self):
        #while True:
        #   print "By"
        pass
