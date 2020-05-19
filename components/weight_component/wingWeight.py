import numpy as np

from openmdao.api import ExplicitComponent


class wingWeightComp(ExplicitComponent):

    def initialize(self):
        self.options.declare('N', types=float)
        self.options.declare('tc', types=float)
        self.options.declare('AR', types=float)
        self.options.declare('sweep', types=float)
        #self.options.declare('taper', types=float)

    def setup(self):
        self.add_input('W0')
        self.add_input('Swing')
        self.add_output('Wwing')

        self.declare_partials('Wwing', 'W0')
        self.declare_partials('Wwing', 'Swing')

    def compute(self, inputs, outputs):
        N = self.options['N']
        tc = self.options['tc']
        AR = self.options['AR']
        sweep = self.options['sweep']
        #taper = self.options['taper']

        W0 = inputs['W0']
        Swing = inputs['Swing']

        cosSweep = np.cos(sweep * np.pi / 180)

        outputs['Wwing'] = 0.0051 * W0 ** 0.557 * N ** 0.557 * Swing ** 0.649 * AR ** 0.5 * tc ** -0.4 * cosSweep ** -1 * 0.1 ** 0.1 * Swing ** 0.1

    def compute_partials(self, inputs, partials):
        N = self.options['N']
        tc = self.options['tc']
        AR = self.options['AR']
        sweep = self.options['sweep']

        W0 = inputs['W0']
        Swing = inputs['Swing']

        cosSweep = np.cos(sweep * np.pi / 180)

        partials['Wwing', 'W0'] = 0.0051 * 0.557 * W0 ** -0.443 * N ** 0.557 * Swing ** 0.649 * AR ** 0.5 * tc ** -0.4 * cosSweep ** -1 * 0.1 ** 0.1 * Swing ** 0.1
        partials['Wwing', 'Swing'] = 0.0051 * W0 ** 0.557 * N ** 0.557 * 0.649 * Swing ** -0.351 * AR ** 0.5 * tc ** -0.4 * cosSweep ** -1 * 0.1 ** 0.1 * 0.1 * Swing ** -0.9