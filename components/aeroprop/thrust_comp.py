import numpy as np

from openmdao.api import ExplicitComponent


class thrustComp(ExplicitComponent):

    # def initialize(self):
    #     self.options.declare('BPR', types=float) #bypass ratio
    #     self.options.declare('max_thrust', types=float) #take off thrust
    #     # self.options.declare('g', types=float)

    def setup(self):
        self.add_input('altitude_km')
        self.add_input('BPR')
        self.add_input('max_thrust')
        # self.add_input('lift_to_drag')
        self.add_output('thrust')

        self.declare_partials('thrust', 'altitude_km')
        self.declare_partials('thrust', 'BPR')
        self.declare_partials('thrust', 'max_thrust')
        # self.declare_partials('thrust', 'lift_to_drag')

    def compute(self, inputs, outputs):
        # BPR = self.options['BPR']
        # max_thrust = self.options['max_thrust']
        # # g = self.options['g']

        altitude_km = inputs['altitude_km']
        BPR = inputs['BPR']
        max_thrust = inputs['max_thrust']
        # lift_to_drag = inputs['lift_to_drag']
        outputs['thrust'] = max_thrust * (((0.0013 * BPR) - 0.0397) * altitude_km - (0.0248 * BPR) + 0.7125)

    def compute_partials(self, inputs, partials):
        # BPR = self.options['BPR']
        # max_thrust = self.options['max_thrust']
        # # BPR = self.options['BPR']

        altitude_km = inputs['altitude_km']
        BPR = inputs['BPR']
        max_thrust = inputs['max_thrust']
        # lift_to_drag = inputs['lift_to_drag']

        partials['thrust', 'altitude_km'] = max_thrust * (((0.0013 * BPR) - 0.0397))
        partials['thrust', 'BPR'] = max_thrust * ((0.0013 * altitude_km) - 0.0248)
        partials['thrust', 'max_thrust'] = ((0.0013 * BPR) - 0.0397) * altitude_km - (0.0248 * BPR) + 0.7125
        # partials['thrust', 'lift_to_drag'] = 0