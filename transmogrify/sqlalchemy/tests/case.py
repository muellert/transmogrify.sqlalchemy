# In case anyone ever decides to implement a functional test this may be
# some useful base code

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()

import elkjop.intranet.migrate
import elkjop.intranet.migrate.tests
from elkjop.intranet.migrate.tests.utils import LoadSampleData

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode=True
            zcml.load_config("configure.zcml", elkjop.intranet.migrate)
            zcml.load_config("tests.zcml", elkjop.intranet.migrate.tests)
            fiveconfigure.debug_mode=False

            LoadSampleData("sqlite:///test.db")

        @classmethod
        def tearDown(cls):
            # XXX unlink test.db
            pass

