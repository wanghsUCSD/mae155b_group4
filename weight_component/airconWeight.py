import numpy as np

from openmdao.api import ExplicitComponent


class maingearWeightComp(ExplicitComponent):

    def initialize(self):
        self.options.declare('Np', types=float)
        self.options.declare('Vpr', types=float)

    def setup(self):
        self.add_output('Waircon')

    def compute(self, inputs, outputs):
        Np = self.options['Np']
        Vpr = self.options['Vpr']

        outputs['Waircon'] = 62.36 * Np ** 0.25 * (Vpr / 1000) ** 0.604 * 1000 ** 0.1

