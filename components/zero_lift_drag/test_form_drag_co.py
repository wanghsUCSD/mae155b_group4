import unittest

from .form_drag_co import FormDragCo

from openmdao.api import Problem

from openmdao.utils.assert_utils import assert_check_partials

#  test for Form Factor

class TestFormDragCo(unittest.TestCase):

    def test_component_and_derivatives(self):
        prob = Problem()
        prob.model = FormDragCo()
        prob.setup()
        prob.run_model()

        data = prob.check_partials(out_stream=None)
        assert_check_partials(data, atol=1.e-3, rtol=1.e-3)


if __name__ == '__main__':
    unittest.main()

    #test line