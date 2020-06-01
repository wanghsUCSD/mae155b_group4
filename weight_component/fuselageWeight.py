import numpy as np

from openmdao.api import ExplicitComponent


class fuselageWeightComp(ExplicitComponent):

    def initialize(self):
        self.options.declare('N', types=float)
        self.options.declare('L', types=float)
        self.options.declare('LD', types=float)
        self.options.declare('Sfuse', types=float)
        self.options.declare('sweep', types=float)
        self.options.declare('taper', types=float)

    def setup(self):
        self.add_input('W0')
        self.add_input('Bw')
        self.add_output('Wfuse')

        self.declare_partials('Wfuse', 'W0')

    def compute(self, inputs, outputs):
        N = self.options['N']
        L = self.options['L']
        LD = self.options['LD']
        Sfuse = self.options['Sfuse']
        sweep = self.options['sweep']
        taper = self.options['taper']

        W0 = inputs['W0']
        Bw = inputs['Bw']

        Kws = 0.75 * (1 + 2 * taper) / (1 + taper) * Bw * np.tan(sweep / L * (np.pi / 180))

        outputs['Wfuse'] = 0.328 * 1.12 * W0 ** 0.5 * N ** 0.5  * L ** 0.25 * Sfuse ** 0.302 * (1 + Kws) ** 0.04 * LD ** 0.1

    def compute_partials(self, inputs, partials):
        N = self.options['N']
        L = self.options['L']
        LD = self.options['LD']
        Sfuse = self.options['Sfuse']
        sweep = self.options['sweep']
        taper = self.options['taper']

        W0 = inputs['W0']
        Bw = inputs['Bw']

        Kws = 0.75 * (1 + 2 * taper) / (1 + taper) * Bw * np.tan(sweep / L * (np.pi / 180))

        partials['Wfuse', 'W0'] = 0.328 * 1.12 * 0.5 * W0 ** -0.5 * N ** 0.5 * L ** 0.25 * Sfuse ** 0.302 * (1 + Kws) ** 0.04 * LD ** 0.1

       