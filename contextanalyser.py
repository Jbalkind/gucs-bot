#
# Purpose: Conextual Analyser for the simple language parsed by simpleparser.py
# Created by Craig McL on 26/12/2011
# Last Edited by Craig McL on 27/12/2011
#

from nsmanager import *
from namespace import *
import inspect
import copy

class ContextError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return "{}".format(self.msg)

class ContextAnalyser(object):
    def __init__(self):
        """Initialises the Namespace Manager object.

        Creates and initialises a builtin namespace which is passed to
        the NSManager object as the initial namespaces available to users.
        """
        self.builtinOwner = "BUILTIN"
        self.nsmanager = NSManager({"builtins" : NameSpace("builtins",
                                                  [self.builtinOwner], True)})
        self.builtin = self.nsmanager.get_ns(self.builtinOwner, "builtins")

    def __getattribute__(self, name):
        """Perform operation methods so they all catch Namespace Exceptions."""
        attr = object.__getattribute__(self, name)
        if inspect.ismethod(attr) and (not name.startswith("__")):
            def f(*args):
                try:
                    return attr(*args)
                except NameSpaceError as nserror:
                    raise ContextError(nserror)
            return f
        return attr
    
    def get_ident(self, user, ident):
        try:
            result = self.nsmanager.get_user_ns(user).get_ident(ident)
        except NSUndefinedIdentiferError as e:
            return self.builtin.get_ident(ident)
        else:
            return result
    
    def add_ident(self, user, ident, value):
        return self.nsmanager.get_user_ns(user).add_ident(ident, value)
    
    def create_ns(self, name, user, access):
        ns = NameSpace(name, [user], access)
        self.nsmanager.create_ns(name, ns)

    def change_ns(self, user, namespace):
        return self.nsmanager.set_user_ns(user, namespace)

    def share_ns(self, owner, user, namespace):
        """Add user to namespace with owner as an owner of the namespace."""
        ns = self.nsmanager.get_ns(owner, namespace)
        return ns.add_owner(user)
        
    def get_ns_name(self, user):
        """Returns the name of the namespace the user is currently using."""
        return self.nsmanager.get_user_ns(user).get_name()
