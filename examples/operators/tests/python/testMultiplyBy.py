import unittest

from streamsx.topology.topology import *
from streamsx.topology.tester import Tester
import streamsx.spl.op as op
import streamsx.spl.toolkit as tk
import numpy as np

class TestMultiplyByStandalone(unittest.TestCase):
    """Class for driving the test in standalone mode"""

    def setUp(self):
        """Set up to run test as Standalone"""
        Tester.setup_standalone(self)

    def _add_toolkits(self, topo):
        # Add required toolkits for test to run
        tk.add_toolkit(topo, '../../examples.operators')
        tk.add_toolkit(topo, '../examples.operators.testing')

    def test_op(self):
        """ Test the operator using a test composite for data generation. """
        topo = Topology()
        self._add_toolkits(topo)

        # Set up parameter to call the test composite,
        # in this case multiplying by three, the same
        # factor is used in the conditions set up for the test
        factor = 3
        params = {'factor':factor}

        # Call the test composite
        test_op = op.Source(topo, 'examples.operators.testing::TestMultiplyBy',
            'tuple<int32 result>', params=params)

        # Set up Tester to validate the result of running the test composite
        tester = Tester(topo)

        # Example to check for tuple count
        tester.tuple_count(test_op.stream, 34)

        # Example to check content of the stream with an expected list of data
        # Use map to covert the SPL tuple with a single attribute into
        # a stream of ints.
        mapped = test_op.stream.map(lambda x: x['result'])
        expected = list(np.arange(0, 100, factor))
        tester.contents(mapped, expected)

        # Example to check data tuple by tuple
        # The callable passed into tuple_check will be called
        # for each tuple on the stream.
        # If the callable returns False then the test will fail.
        # The SPL tuple is passed in a dict with the keys being the
        # attribute names
        tester.tuple_check(test_op.stream, lambda x: x['result'] % factor == 0)

        # Runs the test, a failure will cause an assertion to be raised
        tester.test(self.test_ctxtype, self.test_config)


class TestMultiplyByDistributed(TestMultiplyByStandalone):
    """Example to run the same test in distributed mode"""
    def setUp(self):
        Tester.setup_distributed(self)


#class TestFTPCloud(TestFTP):
#    """ Test invocations of FTP operators with streaming analytics """
#    def setUp(self):
#        Tester.setup_streaming_analytics(self, force_remote_build=True)
