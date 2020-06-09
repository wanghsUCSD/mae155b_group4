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
        self.add_input('isp') 
        self.add_input('W0')
        self.add_output('w_frac')

        self.declare_partials('w_frac', 'speed')
        self.declare_partials('w_frac', 'LD')
        self.declare_partials('w_frac', 'rnge')
        self.declare_partials('w_frac', 'W0')
        self.declare_partials('w_frac', 'isp')

    def compute(self, inputs, outputs):

        speed = inputs['speed']
        LD = inputs['LD']
        rnge = inputs['rnge']
        isp = inputs['isp']
        W0 = inputs['W0']

        outputs['w_frac'] = W0 / (np.exp(rnge / (speed * LD * isp)))

    def compute_partials(self, inputs, partials):
        speed = inputs['speed']
        LD = inputs['LD']
        rnge = inputs['rnge']
        isp = inputs['isp']
        W0 = inputs['W0']

        partials['w_frac', 'speed'] = (rnge*W0*np.exp(-1*rnge/(LD*speed*isp)))/(LD*(speed**2)*isp)
        partials['w_frac', 'LD'] = (rnge * W0 * np.exp(-1*rnge/(speed*LD*isp))) / speed * (LD**2) * isp
        partials['w_frac', 'rnge'] = (-1 * W0 * np.exp(-1*rnge/(LD*speed*isp))) / (LD * speed * isp)
        partials['w_frac', 'isp'] = (rnge * W0 * np.exp(-1*rnge/(LD*speed*isp))) / LD * speed * (isp**2)
        partials['w_frac', 'W0'] = 1 / ( np.exp(rnge/(speed * LD * isp)))


