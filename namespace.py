#
# Purpose: Defines a NameSpace class and associated Exception classes
# Created by Craig McL (CMCL) <mistercouk@gmail.com> on 26/12/2011
# Last edited by Craig McL on 27/12/2011
#

class NameSpaceError(Exception):
    def __init__(self):
        pass
    
class NSUndefinedIdentiferError(NameSpaceError):
    def __init__(self, ident, namespaceName):
        self.ident = ident
        self.nsName = namespaceName

    def __str__(self):
        return "Undefined identifer '{}' in namespace '{}'".format(
            self.ident, self.nsName)

class NameSpace(object):
    def __init__(self, name, owners, public=False):
        self.name = name
        self.space = {}
        self.owners = [] if owners is None else owners
        self.public = public

    def get_name(self):
        return self.name

    def set_public(self, value):
        self.public = value

    def is_public(self):
        return self.public

    def is_owner(self, user):
        return user in self.owners

    def add_owner(self, user):
        self.owners.append(user)
        return user

    def add_ident(self, ident, value):
        self.space[ident] = value
        return value

    def get_ident(self, ident):
        if self.space.get(ident, None):
            return self.space[ident]
        else:
            raise NSUndefinedIdentiferError(ident, self.name)
