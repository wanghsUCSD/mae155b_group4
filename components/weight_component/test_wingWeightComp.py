import unittest

from .wingWeight import wingWeightComp
from openmdao.api import Problem
from openmdao.utils.assert_utils import assert_check_partials


class TestWingWeightComp(unittest.TestCase):

    def test_component_and_derivatives(self):
        prob = Problem()
        prob.model = wingWeightComp(N=3.,tc=0.3,AR=9.,sweep=30.)
        prob.setup()
        prob.run_model()

        data = prob.check_partials(out_stream=None)
        assert_check_partials(data, atol=1.e2, rtol=1.e2)


if __name__ == '__main__':
    unittest.main()