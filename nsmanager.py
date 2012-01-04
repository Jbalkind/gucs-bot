#
#
# Created by Craig McL on 26/12/2011
# Last Edited by Craig McL on 26/12/2011
#
#

from namespace import NameSpace, NameSpaceError

class UndefinedNameSpaceError(NameSpaceError):
    def __init__(self, ns):
        self.ns = ns
    def __str__(self):
        return "NameSpace '{}' is not defined.".format(self.ns)

class NameSpaceAccessDeniedError(NameSpaceError):
    def __init__(self, owner, namespace):
        self.owner = owner
        self.namespace = namespace

    def __str__(self):
        string = "User '{}' does not have owner permission for Namespace '{}'"
        return string.format(self.owner, self.namespace)

class NSManager(object):
    def __init__(self, initialNamespaces):
        """Creates namespace mappings.

        Two mappings exist:
            * Name of Namespace : Namespace object
            * Name of User : Current Namespace object in use by user.
        The first mapping is initialised to a dictionary of namespaces
        passed in as an argument to this constructor.
        """
        # Mapping from namespace name to NameSpace.
        self.namespaces = initialNamespaces
        # Mapping from usernames to their currently used namespaces
        self.activeSpaces = {}

    def get_user_ns(self, user):
        if self.activeSpaces.get(user, None):
            return self.activeSpaces[user]
        else:
            # Create new namespace
            ns = NameSpace(user, [user], False)
            self.activeSpaces[user] = ns
            self.namespaces[user] = ns
            return ns

    def set_user_ns(self, user, namespace):
        if self.namespaces.get(namespace, None):
            ns = self.namespaces[namespace]
            if ns.is_owner(user) or ns.is_public():
                self.activeSpaces[user] = self.namespaces[namespace]
                return self.activeSpaces[user]
            else:
                raise NameSpaceAccessDeniedError(user, namespace)
        else:
            raise UndefinedNameSpaceError(namespace)

    def create_ns(self, name, namespace):
        self.namespaces[name] = namespace

    def get_ns(self, owner, namespace):
        ns = self.namespaces.get(namespace, None)
        if ns:
            if ns.is_owner(owner):
                return ns
            else:
                raise NameSpaceAccessDeniedError(owner, namespace)
        else:
            raise UndefinedNameSpaceError(namespace)
