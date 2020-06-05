import numpy as np

from openmdao.api import ExplicitComponent


class wingWeightComp(ExplicitComponent):

    def initialize(self):
        self.options.declare('N', types=float)
        self.options.declare('tc', types=float)
        self.options.declare('AR', types=float)
        self.options.declare('sweep', types=float)
        self.options.declare('taper', types=float)

    def setup(self):
        self.add_input('W0')
        self.add_input('S_wing')
        self.add_output('W_wing')

        self.declare_partials('W_wing', 'W0')
        self.declare_partials('W_wing', 'S_wing')

    def compute(self, inputs, outputs):
        N = self.options['N']
        tc = self.options['tc']
        AR = self.options['AR']
        sweep = self.options['sweep']
        taper = self.options['taper']

        W0 = inputs['W0']
        S_wing = inputs['S_wing']

        cosSweep = np.cos(sweep * (np.pi / 180))

        outputs['W_wing'] = 0.0051 * W0 ** 0.557 * N ** 0.557 * S_wing ** 0.649 * AR ** 0.5 * tc ** -0.4 * (1 + taper) ** 0.1 * cosSweep ** -1 * 0.2 ** 0.1 * S_wing ** 0.1

    def compute_partials(self, inputs, partials):
        N = self.options['N']
        tc = self.options['tc']
        AR = self.options['AR']
        sweep = self.options['sweep']
        taper = self.options['taper']

        W0 = inputs['W0']
        S_wing = inputs['S_wing']

        cosSweep = np.cos(sweep * np.pi / 180)

        partials['W_wing', 'W0'] = 0.0051 * 0.557 * W0 ** -0.443 * N ** 0.557 * S_wing ** 0.649 * AR ** 0.5 * tc ** -0.4 * (1 + taper) ** 0.1 * cosSweep ** -1 * 0.2 ** 0.1 * S_wing ** 0.1
        partials['W_wing', 'S_wing'] = 0.0051 * W0 ** 0.557 * N ** 0.557 * 0.649 * S_wing ** -0.351 * AR ** 0.5 * tc ** -0.4 * (1 + taper) ** 0.1 * cosSweep ** -1 * 0.2 ** 0.1 * 0.1 * S_wing ** -0.9