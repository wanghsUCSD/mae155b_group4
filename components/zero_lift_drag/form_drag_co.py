import numpy as np
from openmdao.api import ExplicitComponent

# 
#    Computes the Form Factor which takes into account the interference drag
# 

class FormDragCo(ExplicitComponent):

    def setup(self):
        # inputs for wing form factor

        self.add_input('t_c')
        # # x_t is the position of maximum thickness
        
        self.add_input('x_t')
        self.add_input('mach_number')
        self.add_input('sweep_angle')
        self.add_output('FF_wing')

        # inputs for fuselage form factor
        # finesse ratio is length / diameter of thing being looked at
        self.add_input('fuselage_finesse_ratio')
        self.add_output('FF_fuselage')
        # inputs for nacelle form factor
        self.add_input('naselle_finesse_ratio')
        self.add_output('FF_nacelle')
        # declare partials for FF_wing with respect to t_c, mach, x_t, and sweep angle

        self.declare_partials('FF_wing', 't_c')
        self.declare_partials('FF_wing', 'mach_number')
        self.declare_partials('FF_wing', 'x_t')
        self.declare_partials('FF_wing', 'sweep_angle')

        # declare partials for FF_fuselage with respect to its finesse ratio
        self.declare_partials('FF_fuselage', 'fuselage_finesse_ratio')
        # declare partials for FF_nacelle with respect to its finesse ratio
        self.declare_partials('FF_nacelle', 'naselle_finesse_ratio')
        
        
    def compute(self, inputs, outputs):
        t_c = inputs['t_c']
        x_t = inputs['x_t']
        mach_number = inputs['mach_number']
        sweep_angle = inputs['sweep_angle']
        # fuselage terms
        fuselage_finesse_ratio = inputs['fuselage_finesse_ratio']
        # nacelle terms
        naselle_finesse_ratio = inputs['naselle_finesse_ratio']
        
        # compute equations for FF
        outputs['FF_wing'] = (1+ (0.6/x_t)*(t_c) + 100 *t_c**4)*(1.34*mach_number**0.18 * np.cos(sweep_angle)**0.28)
        outputs['FF_fuselage'] = 1 + 60/(fuselage_finesse_ratio**3) + fuselage_finesse_ratio/400
        outputs['FF_nacelle'] = 1 + (0.35/naselle_finesse_ratio)

    def compute_partials(self, inputs, partials):
        t_c = inputs['t_c']
        x_t = inputs['x_t']
        mach_number = inputs['mach_number']
        sweep_angle = inputs['sweep_angle']
        # fuselage terms
        fuselage_finesse_ratio = inputs['fuselage_finesse_ratio']
        # nacelle terms
        naselle_finesse_ratio = inputs['naselle_finesse_ratio']


        partials['FF_wing', 't_c'] = 536*mach_number**0.18 *np.cos(sweep_angle)**0.28 * (t_c**3 *x_t + 0.0015)/x_t
        partials['FF_wing', 'x_t'] = -0.804*t_c*mach_number**0.18 *np.cos(sweep_angle)**0.28 / x_t**2
        partials['FF_wing', 'mach_number'] = 0.2412*np.cos(sweep_angle)**0.28 * (1+ (0.6/x_t)*(t_c) + 100 *t_c**4)
        partials['FF_wing', 'sweep_angle'] = -0.3752*mach_number**0.18*np.sin(sweep_angle) * (1+ (0.6/x_t)*(t_c) + 100 *t_c**4) / np.cos(sweep_angle)**0.72

        partials['FF_fuselage', 'fuselage_finesse_ratio'] = -180 / (fuselage_finesse_ratio**4) + 1/400
        partials['FF_nacelle', 'naselle_finesse_ratio'] = -0.35 / (naselle_finesse_ratio**2)

        