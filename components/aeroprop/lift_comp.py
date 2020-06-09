import numpy as np

from openmdao.api import ExplicitComponent


class liftComp(ExplicitComponent):

    # def initialize(self):
    #     self.options.declare('Cl', types=float)

    def setup(self):
        self.add_input('speed')
        self.add_input('density')
        self.add_input('Cl')
        self.add_input('S_w')
        self.add_output('lift')

        self.declare_partials('lift', 'speed')
        self.declare_partials('lift', 'density')
        self.declare_partials('lift', 'Cl')
        self.declare_partials('lift', 'S_w')

    def compute(self, inputs, outputs):
        # Cl = self.options['Cl']

        speed = inputs['speed']
        density = inputs['density']
        Cl = inputs['Cl']
        S_w = inputs['S_w']
        outputs['lift'] = Cl * 0.5 * speed ** 2 * density * S_w

    def compute_partials(self, inputs, partials):
        # Cl = self.options['Cl']

        speed = inputs['speed']
        density = inputs['density']
        Cl = inputs['Cl']
        S_w = inputs['S_w']

        partials['lift', 'speed'] = Cl * density * speed * S_w
        partials['lift', 'density'] = Cl * 0.5 * speed ** 2 * S_w
        partials['lift', 'Cl'] = density * 0.5 * speed ** 2 * S_w
        partials['lift', 'S_w'] = Cl * density * 0.5 * speed ** 2