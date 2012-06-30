import types
from unittest import TestCase
from unittest import TestSuite
from unittest import makeSuite
from transmogrify.sqlalchemy import SQLSourceSection
from transmogrify.sqlalchemy.tests.utils import LoadSampleData


class MockTransmogrifier(object):
    pass


class SQLSourceSectionTests(TestCase):
    def setUp(self):
        options=dict(query1="SELECT * FROM menu",
                     query2="SELECT * FROM menu WHERE id=1",
                     dsn="sqlite://",
                     blueprint='blueprintname')
        self.source=SQLSourceSection(MockTransmogrifier(), None, options, [])
        LoadSampleData(self.source.connection)


    def testIsAGenerator(self):
        self.assertEqual(type(self.source.__iter__()), types.GeneratorType)

    def testReturnsDictionary(self):
        data=[row for row in self.source]
        self.failUnless(isinstance(data[0], dict))

    def testReturnedData(self):
        data=[row for row in self.source]
        self.assertEqual(data,
                [{u"price": 25, u"id": 1, u"title": u"Cream Spinach Soup"},
                 {u"price": 37, u"id": 2, u"title": u"Shrimp Toast"},
                 {u"price": 34, u"id": 3, u"title": u"Mini eggrolls"},
                 {u"price": 25, u"id": 1, u"title": u"Cream Spinach Soup"}])

    def testUnknownTableReturnsEmptyList(self):
        # No SQLAlchemy internal errors should be exposed
        self.source.queries=["SELECT * FROM nothere"]
        data=[row for row in self.source]
        self.assertEqual(data, [])

    def testSQLSyntaxErrorReturnsEmptyList(self):
        # No SQLAlchemy internal errors should be exposed
        self.source.queries=["INVALID COMMAND"]
        data=[row for row in self.source]
        self.assertEqual(data, [])


def test_suite():
    suite=TestSuite()
    suite.addTest(makeSuite(SQLSourceSectionTests))
    return suite
