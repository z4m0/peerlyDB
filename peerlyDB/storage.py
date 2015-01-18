import time
from itertools import izip
from itertools import imap
from itertools import takewhile
import operator
from collections import OrderedDict

from zope.interface import implements
from zope.interface import Interface

from peerlyDB.utils import digest
from peerlyDB.log import Logger
import json, base64

class IStorage(Interface):
    """
    Local storage for this node.
    """

    def __setitem__(key, value):
        """
        Set a key to the given value.
        """

    def __getitem__(key):
        """
        Get the given key.  If item doesn't exist, raises C{KeyError}
        """

    def get(key, default=None):
        """
        Get given key.  If not found, return default.
        """

    def iteritemsOlderThan(secondsOld):
        """
        Return the an iterator over (key, value) tuples for items older than the given secondsOld.
        """

    def iteritems():
        """
        Get the iterator for this storage, should yield tuple of (key, value)
        """


class ForgetfulStorage(object):
    implements(IStorage)

    def __init__(self, ttl=604800, keySize=50):
        """
        By default, max age is a week.
        Only remembers last 50 values for a given key
        """
        self.data = OrderedDict()
        self.ttl = ttl
        self.keySize = keySize
        self.log = Logger(system=self)

    def __setitem__(self, key, value):
        self.log.debug('Setting value %s of type %s' % (str(value),type(value)))
        if isinstance(value,str):
          value = json.loads(value) #TODO put this in a try and check elif dictionary
        #if a full key is sent to us...
        if self._isVersionsValue(value):
            self.log.debug('Got versions value for value:%s' % (str(value)))
            if not (key in self.data):
              self.data[key] = {}
            #Merge the two versions
            self.data[key] = OrderedDict(sorted(value.items()+self.data[key].items(), key=lambda t: t[0]))
            #TODO remove the first elements if size > self.keySize
            return
        
        self.log.debug('The value has not versions')
        #create a new version
        if not (key in self.data):
            self.data[key] = OrderedDict()
        dig = base64.b64encode(digest(value))
        
        #if value already exists, just refresh it
        for date, (d,v) in self.data[key].iteritems():
            if(d == dig):
                del self.data[key][date]
                break
        self.data[key][str(time.time())] = (dig,value)
        if len (self.data[key]) > self.keySize:
            self.data[key].popitem(last=False)
        self.cull()
        
    def _isVersionsValue(self,value):
    #A versions value is a dictionary all made of versions
        try:
          for k in value:
            float(k)
        except ValueError:
          return False
        return True
    
    def cull(self):
        pass
        #Let's ignore this for now...
        #for k, v in self.iteritemsOlderThan(self.ttl):
        #    self.data.popitem(last=False)

    def get(self, key, default=None):
        self.cull()
        if key in self.data:
            return self[key]
        return default

    def __getitem__(self, key):
        self.cull()
        return str(json.dumps(self.data[key]))

    def __iter__(self):
        self.cull()
        return iter(self.data)

    def __repr__(self):
        self.cull()
        return repr(self.data)

    def iteritemsOlderThan(self, secondsOld):
        minBirthday = time.time() - secondsOld
        zipped = self._tripleIterable()
        matches = takewhile(lambda r: minBirthday >= r[1], zipped)
        return imap(operator.itemgetter(0, 2), matches)

    def _tripleIterable(self):
        ikeys = self.data.iterkeys()
        ibirthday = imap(operator.itemgetter(0), self.data.itervalues())
        ivalues = imap(operator.itemgetter(1), self.data.itervalues())
        return izip(ikeys, ibirthday, ivalues)

    def iteritems(self):
        self.cull()
        ikeys = self.data.iterkeys()
        ivalues = imap(operator.itemgetter(1), self.data.itervalues())
        return izip(ikeys, ivalues)
