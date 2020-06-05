import numpy as np

from openmdao.api import ExplicitComponent


class hydraulicWeightComp(ExplicitComponent):

    def setup(self):
        self.add_input('Bw')
        self.add_output('W_hydraulic')

        self.declare_partials('W_hydraulic', 'Bw')

    def compute(self, inputs, outputs):
        Bw = inputs['Bw']

        outputs['W_hydraulic'] = 0.2673 * 5 * (205 + Bw) ** 0.937

    def compute_partials(self, inputs, partials):
        Bw = inputs['Bw']

        partials['W_hydraulic', 'Bw'] =0.2673 * 5 * 0.937 * (205 + Bw) ** -0.063
