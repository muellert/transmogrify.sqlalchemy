import copy
from zope.interface import classProvides, implements
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.interfaces import ISection

_store = []

def clearStore():
    _store[:]=[]

def getStore():
    return _store


class MemoryStore(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous

    def __iter__(self):
        global _store

        for item in self.previous:
            _store.append(copy.deepcopy(item))
            yield item


def LoadSampleData(connection):
    connection.execute("""CREATE TABLE menu (
                                id INT,
                                title VARCHAR(64),
                                price INT);""")
    connection.execute("INSERT INTO menu VALUES (1, 'Cream Spinach Soup', 25)")
    connection.execute("INSERT INTO menu VALUES (2, 'Shrimp Toast', 37)")
    connection.execute("INSERT INTO menu VALUES (3, 'Mini eggrolls', 34)")
