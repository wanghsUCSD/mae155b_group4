import numpy as np

from openmdao.api import ExplicitComponent


class dragComp(ExplicitComponent):

    # def initialize(self):
    #     self.options.declare('Cd', types=float)

    def setup(self):
        self.add_input('speed')
        self.add_input('density')
        self.add_input('Cd')
        self.add_input('S_w')
        self.add_output('drag')

        self.declare_partials('drag', 'speed')
        self.declare_partials('drag', 'density')
        self.declare_partials('drag', 'Cd')
        self.declare_partials('drag', 'S_w')

    def compute(self, inputs, outputs):
        # Cd = self.options['Cd']

        speed = inputs['speed']
        density = inputs['density']
        Cd = inputs['Cd']
        S_w = inputs['S_w']
        outputs['drag'] = Cd * 0.5 * speed ** 2 * density * S_w

    def compute_partials(self, inputs, partials):
        # Cd = self.options['Cd']

        speed = inputs['speed']
        density = inputs['density']
        Cd = inputs['Cd']
        S_w = inputs['S_w']

        partials['drag', 'speed'] = Cd * density * speed * S_w
        partials['drag', 'density'] = Cd * 0.5 * speed ** 2 * S_w
        partials['drag', 'Cd'] = density * 0.5 * speed ** 2 * S_w
        partials['drag', 'S_w'] = Cd * density * 0.5 * speed ** 2