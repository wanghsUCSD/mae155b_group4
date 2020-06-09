import numpy as np

from openmdao.api import ExplicitComponent


class liftComp(ExplicitComponent):

    # def initialize(self):
    #     self.options.declare('Cl', types=float)

    def setup(self):
        self.add_input('speed')
        self.add_input('density')
        self.add_input('Cl')
        self.add_output('lift')

        self.declare_partials('lift', 'speed')
        self.declare_partials('lift', 'density')
        self.declare_partials('lift', 'Cl')

    def compute(self, inputs, outputs):
        # Cl = self.options['Cl']

        speed = inputs['speed']
        density = inputs['density']
        Cl = inputs['Cl']
        outputs['lift'] = Cl * 0.5 * speed ** 2 * density * 50

    def compute_partials(self, inputs, partials):
        # Cl = self.options['Cl']

        speed = inputs['speed']
        density = inputs['density']
        Cl = inputs['Cl']

        partials['lift', 'speed'] = 50 * Cl * density * speed
        partials['lift', 'density'] = 50 * Cl * 0.5 * speed ** 2
        partials['lift', 'Cl'] = 50 * 0.5 * speed ** 2