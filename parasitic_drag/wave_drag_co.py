import numpy as np

from openmdao.api import ExplicitComponent

# 
#    Computes the Wave Drag Coefficient using Cruising Mach number and Critical Mach Number as inputs.
# 


class WaveDragCo(ExplicitComponent):

    def array_setup(self):
        self.add_input('mach_number')
        self.add_input('critical_mach_number')
        self.add_output('wave_drag_co')

        self.declare_partials('wave_drag_co', 'mach_number')
        self.declare_partials('wave_drag_co', 'critical_mach_number')

    def compute(self, inputs, outputs):
        d_mach = inputs['mach_number'] - inputs['critical_mach_number']
        d_mach *= d_mach > 0.1

        outputs['wave_drag_coeff'] = 20. * d_mach ** 4

    def compute_partials(self, inputs, partials):
        d_mach = (inputs['mach_number'] - inputs['critical_mach_number']).flatten()
        d_mach *= d_mach > 0.1

        partials['wave_drag_co', 'mach_number'] = 80. * d_mach ** 3
        partials['wave_drag_co', 'critical_mach_number'] = -80. * d_mach ** 3