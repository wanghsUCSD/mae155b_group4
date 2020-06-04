import numpy as np

from openmdao.api import ExplicitComponent

# 
# The final form of the breguet range equation
# NEEDED COMPONENT INPUTS: L/D


class BregRangeCo(ExplicitComponent):

    def setup(self):
        self.add_input('speed')
        self.add_input('LD')
        self.add_input('rnge')
        self.add_input('isp') #This is a dummy variable for ISP
        self.add_output('w_frac')

        self.declare_partials('w_frac', 'speed')
        self.declare_partials('w_frac', 'LD')
        self.declare_partials('w_frac', 'rnge')
        self.declare_partials('w_frac', 'isp')

    def compute(self, inputs, outputs):

        speed = inputs['speed']
        LD = inputs['LD']
        rnge = inputs['rnge']
        isp = inputs['isp']

        outputs['w_frac'] = np.exp(rnge / (speed * LD * isp))

    def compute_partials(self, inputs, partials):
        speed = inputs['speed']
        LD = inputs['LD']
        rnge = inputs['rnge']
        isp = inputs['isp']

        partials['w_frac', 'speed'] = ((-1) * rnge / (speed**2 * LD * isp)) * np.exp(rnge / (speed * LD * isp))
        partials['w_frac', 'LD'] = ((-1) * rnge / (speed * (LD**2) * isp)) * np.exp(rnge / (speed * LD * isp))
        partials['w_frac', 'rnge'] = (1 / (speed * LD * isp)) * np.exp(rnge / (speed * LD * isp))
        partials['w_frac', 'isp'] = ((-1) * rnge / (speed * LD * isp**2)) * np.exp(rnge / (speed * LD * isp))    

