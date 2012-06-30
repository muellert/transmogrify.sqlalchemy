import logging
import sqlalchemy
from sqlalchemy.exceptions import OperationalError
from zope.interface import classProvides, implements
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.interfaces import ISection


class SQLSourceSection(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.logger = logging.getLogger(options['blueprint'])
        
        keys = options.keys()
        keys.sort()
        self.queries = [options[k] for k in keys if k.startswith('query')]
        
        # Allow for connection reuse along a pipeline
        dsn = options['dsn']
        if hasattr(transmogrifier, '_sqlsource_connections'):
            conns = transmogrifier._sqlsource_connections
        else:
            transmogrifier._sqlsource_connections = conns = {}
            
        if dsn in conns:
            self.connection = conns[dsn]
        else:
            engine = sqlalchemy.create_engine(dsn)
            conns[dsn] = self.connection = engine.connect()

    def __iter__(self):
        for item in self.previous:
            yield item
            
        trans=self.connection.begin()
        try:
            for query in self.queries:
                result=self.connection.execute(query)
                for row in result:
                    yield dict((x[0].encode('utf-8'), x[1]) for x in row.items())
            trans.commit()
        except OperationalError, e:
            trans.rollback()
            self.logger.warn("SQL operational error: %s" % e)
        except:
            trans.rollback()
            raise

