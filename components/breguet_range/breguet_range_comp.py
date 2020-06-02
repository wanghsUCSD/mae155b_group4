import numpy as np

from openmdao.api import ExplicitComponent

# 
# The final form of the breguet range equation
# NEEDED COMPONENT INPUTS: L/D


class BregRangeCo(ExplicitComponent):

    def setup(self):
        self.add_input('sonic_speed')
        self.add_input('LD')
        self.add_input('rnge')
        self.add_input('isp') #This is a dummy variable for ISP
        self.add_output('w_frac')

        self.declare_partials('w_frac', 'sonic_speed')
        self.declare_partials('w_frac', 'LD')
        self.declare_partials('w_frac', 'rnge')
        self.declare_partials('w_frac', 'isp')

    def compute(self, inputs, outputs):

        sonic_speed = inputs['sonic_speed']
        LD = inputs['LD']
        rnge = inputs['rnge']
        isp = inputs['isp']

        outputs['w_frac'] = np.exp(rnge / (sonic_speed * LD * isp))

    def compute_partials(self, inputs, partials):
        sonic_speed = inputs['sonic_speed']
        LD = inputs['LD']
        rnge = inputs['rnge']
        isp = inputs['isp']

        partials['w_frac', 'sonic_speed'] = ((-1) * rnge / (sonic_speed**2 * LD * isp)) * np.exp(rnge / (sonic_speed * LD * isp))
        partials['w_frac', 'LD'] = ((-1) * rnge / (sonic_speed * (LD**2) * isp)) * np.exp(rnge / (sonic_speed * LD * isp))
        partials['w_frac', 'rnge'] = (1 / (sonic_speed * LD * isp)) * np.exp(rnge / (sonic_speed * LD * isp))
        partials['w_frac', 'isp'] = ((-1) * rnge / (sonic_speed * LD * isp**2)) * np.exp(rnge / (sonic_speed * LD * isp))    

