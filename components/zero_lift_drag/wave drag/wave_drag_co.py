import numpy as np
from openmdao.api import ExplicitComponent
import openmdao.api as om

# 
#    Computes the Wave Drag Coefficient using Cruising Mach number and Critical Mach Number as inputs.
# 


class WaveDragCo(ExplicitComponent):

    def setup(self):
        self.add_input('mach_number')
        self.add_input('critical_mach_number')
        self.add_output('wave_drag_co')


        self.declare_partials('wave_drag_co', 'mach_number')
        self.declare_partials('wave_drag_co', 'critical_mach_number')

    def compute(self, inputs, outputs):
        d_mach = inputs['mach_number'] - inputs['critical_mach_number']
        d_mach *= d_mach > 0.1

        outputs['wave_drag_co'] = 20. * d_mach ** 4

    def compute_partials(self, inputs, partials):
        d_mach = (inputs['mach_number'] - inputs['critical_mach_number']).flatten()
        d_mach *= d_mach > 0.1

        partials['wave_drag_co', 'mach_number'] = 80. * d_mach ** 3
        partials['wave_drag_co', 'critical_mach_number'] = -80. * d_mach ** 3

# runs a test to see if calculated values make sense
if __name__ == "__main__":
    model = om.Group()
    ivc = om.IndepVarComp()
    ivc.add_output('mach_number', 0.85)
    ivc.add_output('critical_mach_number', 0.75)

    model.add_subsystem('des_vars', ivc)
    model.add_subsystem('wave_drag', WaveDragCo())

    model.connect('des_vars.mach_number', 'wave_drag.mach_number')
    model.connect('des_vars.critical_mach_number', 'wave_drag.critical_mach_number')

    prob = om.Problem(model)
    prob.setup()
    prob.run_model()
    print('Wave Drag Coefficient')
    print(prob['wave_drag.wave_drag_co'])