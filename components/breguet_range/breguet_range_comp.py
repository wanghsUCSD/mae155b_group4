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
        self.add_output('W_f')

        self.declare_partials('W_f', 'speed')
        self.declare_partials('W_f', 'LD')
        self.declare_partials('W_f', 'rnge')
        self.declare_partials('W_f', 'W0')
        self.declare_partials('W_f', 'isp')

    def compute(self, inputs, outputs):

        speed = inputs['speed']
        LD = inputs['LD']
        rnge = inputs['rnge']
        isp = inputs['isp']
        W0 = inputs['W0']

        outputs['W_f'] = W0 / (np.exp(rnge / (speed * LD * isp)))

    def compute_partials(self, inputs, partials):
        speed = inputs['speed']
        LD = inputs['LD']
        rnge = inputs['rnge']
        isp = inputs['isp']
        W0 = inputs['W0']

        partials['W_f', 'speed'] = (rnge*W0*np.exp(-1*rnge/(LD*speed*isp)))/(LD*(speed**2)*isp)
        partials['W_f', 'LD'] = (rnge * W0 * np.exp(-1*rnge/(speed*LD*isp))) / speed * (LD**2) * isp
        partials['W_f', 'rnge'] = (-1 * W0 * np.exp(-1*rnge/(LD*speed*isp))) / (LD * speed * isp)
        partials['W_f', 'isp'] = (rnge * W0 * np.exp(-1*rnge/(LD*speed*isp))) / LD * speed * (isp**2)
        partials['W_f', 'W0'] = 1 / ( np.exp(rnge/(speed * LD * isp)))


