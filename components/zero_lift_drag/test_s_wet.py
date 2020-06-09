import unittest

from .s_wet import SWet

from openmdao.api import Problem

from openmdao.utils.assert_utils import assert_check_partials

#  test for S_Wet Factor

class TestSWet(unittest.TestCase):

    def test_component_and_derivatives(self):
        prob = Problem()
        prob.model = SWet()
        prob.setup()
        prob.run_model()

        data = prob.check_partials(out_stream=None)
        assert_check_partials(data, atol=1.e-3, rtol=1.e-3)


if __name__ == '__main__':
    unittest.main()

    #test line