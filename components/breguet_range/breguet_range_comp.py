import numpy as np

from openmdao.api import ExplicitComponent

# 
# The final form of the breguet range equation
# NEEDED COMPONENT INPUTS: L/D


class BregRangeCo(ExplicitComponent):

    def setup(self):
        self.add_input('flight_speed', val=257.222)
        self.add_input('LD', val=14) #This is a dummy variable for LD
        self.add_input('R', val=1.296e6)
        self.add_input('isp', val=3000) #This is a dummy variable for ISP
        self.add_output('w_frac')

        self.declare_partials('w_frac', 'flight_speed')
        self.declare_partials('w_frac', 'LD')
        self.declare_partials('w_frac', 'R')
        self.declare_partials('w_frac', 'isp')

    def compute(self, inputs, outputs):

        flight_speed = inputs['flight_speed']
        LD = inputs['LD']
        R = inputs['R']
        isp = inputs['isp']

        outputs['w_frac'] = np.exp(R / (flight_speed * LD * isp))

    def compute_partials(self, inputs, partials):
        flight_speed = inputs['flight_speed']
        LD = inputs['LD']
        R = inputs['R']
        isp = inputs['isp']

        partials['w_frac', 'flight_speed'] = ((-1) * R / (flight_speed**2 * LD * isp)) * np.exp(R / (flight_speed * LD * isp))
        partials['w_frac', 'LD'] = ((-1) * R / (flight_speed * (LD**2) * isp)) * np.exp(R / (flight_speed * LD * isp))
        partials['w_frac', 'R'] = (1 / (flight_speed * LD * isp)) * np.exp(R / (flight_speed * LD * isp))
        partials['w_frac', 'isp'] = ((-1) * R / (flight_speed * LD * isp**2)) * np.exp(R / (flight_speed * LD * isp))    

