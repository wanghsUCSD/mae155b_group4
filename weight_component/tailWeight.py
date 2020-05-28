import numpy as np

from openmdao.api import ExplicitComponent


class htailWeightComp(ExplicitComponent):

    def initialize(self):
        self.options.declare('N', types=float)
        self.options.declare('Lt', types=float)
        self.options.declare('ARht', types=float)
        self.options.declare('sweepht', types=float)
    

    def setup(self):
        self.add_input('W0')
        self.add_input('Sht')
        self.add_output('Wht')

        self.declare_partials('Wht', 'W0')
        self.declare_partials('Wht', 'Sht')

    def compute(self, inputs, outputs):
        N = self.options['N']
        Lt = self.options['Lt']
        ARht = self.options['ARht']
        sweepht = self.options['sweepht']
       

        W0 = inputs['W0']
        Sht = inputs['Sht']

        cosSweepht = np.cos(sweepht * np.pi / 180)
        Ky = 0.3 * Lt

        outputs['Wht'] = 0.0379 * 1.2 ** -0.25 * W0 ** 0.639 * N ** 0.1 * Sht ** 0.75 * Lt ** -1 * Ky ** 0.704 * cosSweepht ** -1 * ARht ** 0.166

    def compute_partials(self, inputs, partials):
        N = self.options['N']
        Lt = self.options['Lt']
        ARht = self.options['ARht']
        sweepht = self.options['sweepht']

        W0 = inputs['W0']
        Sht = inputs['Sht']

        cosSweepht = np.cos(sweepht * np.pi / 180)
        Ky = 0.3 * Lt

        partials['Wht', 'W0'] = 0.0379 * 1.2 ** -0.25 * 0.639 * W0 ** -0.361 * N ** 0.1 * Sht ** 0.75 * Lt ** -1 * Ky ** 0.704 * cosSweepht ** -1 * ARht ** 0.166
        partials['Wht', 'Sht'] = 0.0379 * 1.2 ** -0.25 * W0 ** 0.639 * N ** 0.1 * 0.75 * Sht ** -0.25 * Lt ** -1 * Ky ** 0.704 * cosSweepht ** -1 * ARht ** 0.166

class vtailWeightComp(ExplicitComponent):

    def initialize(self):
        self.options.declare('N', types=float)
        self.options.declare('Lt', types=float)
        self.options.declare('ARvt', types=float)
        self.options.declare('sweepvt', types=float)
        self.options.declare('tc',types=float)
    

    def setup(self):
        self.add_input('W0')
        self.add_input('Svt')
        self.add_output('Wvt')

        self.declare_partials('Wvt', 'W0')
        self.declare_partials('Wvt', 'Svt')

    def compute(self, inputs, outputs):
        N = self.options['N']
        Lt = self.options['Lt']
        ARvt = self.options['ARvt']
        sweepvt = self.options['sweepvt']
        tc = self.options['tc']
       

        W0 = inputs['W0']
        Svt = inputs['Svt']

        cosSweepvt = np.cos(sweepvt * np.pi / 180)
        Kz = Lt

        outputs['Wvt'] = 0.0026 * W0 ** 0.556 * N ** 0.536 * Svt ** 0.5 * Lt ** -0.5 * Kz ** 0.875 * cosSweepvt ** -1 * ARvt ** 0.35 * tc ** -0.5

    def compute_partials(self, inputs, partials):
        N = self.options['N']
        Lt = self.options['Lt']
        ARvt = self.options['ARvt']
        sweepvt = self.options['sweepvt']
        tc = self.options['tc']

        W0 = inputs['W0']
        Svt = inputs['Svt']

        cosSweepvt = np.cos(sweepvt * np.pi / 180)
        Kz = Lt

        partials['Wvt', 'W0'] = 0.0026 * 0.556 * W0 ** -0.444 * N ** 0.536 * Svt ** 0.5 * Lt ** -0.5 * Kz ** 0.875 * cosSweepvt ** -1 * ARvt ** 0.35 * tc ** -0.5
        partials['Wvt', 'Svt'] = 0.0026 * W0 ** 0.556 * N ** 0.536 * 0.5 * Svt ** -0.5 * Lt ** -0.5 * Kz ** 0.875 * cosSweepvt ** -1 * ARvt ** 0.35 * tc ** -0.5
