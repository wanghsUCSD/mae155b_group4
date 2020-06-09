
import numpy as np
from openmdao.api import ExplicitComponent, IndepVarComp
from openmdao.api import Group, Problem
import openmdao.api as om

# 
#    Computes the Wetted Area for Fuselage and Wings
# 

class SWet(ExplicitComponent):

    def setup(self):
        # inputs for S_wet_fuselage

        self.add_input('d_f', val= 6.2) # diameter for fuselage
        self.add_input('l_f', val = 73.9) # length for fuselage
        self.add_input('ln_lf', val = 15.) # The distance from the aircraft nose in x direction to the start of the cylindrical part of the fuselage / l_f
        #  ln_lf just meant to make the partial later easier
        self.add_input('fuselage_finesse_ratio', val = 73.9/6.2) # finesse ratio is length / diameter of thing being looked at
        self.add_output('S_wet_f')

        # inputs for S_wet_wing
        self.add_input('S_w', val = 157.) # Exposed wing area (without including fuselage)
        self.add_input('taper', val = .3) # chord tip / chord root
        self.add_input('t_c', val = 0.14) # thickness to chord ratio at root
        self.add_input('t_c_ratio', val = 1.) # t/c of tip / t/c of root
        self.add_output('S_wet_w')

        # declare partials for wetted areas
        self.declare_partials('S_wet_f', 'd_f')
        self.declare_partials('S_wet_f', 'l_f')
        self.declare_partials('S_wet_f', 'ln_lf')
        self.declare_partials('S_wet_f', 'fuselage_finesse_ratio')

        self.declare_partials('S_wet_w', 'S_w')
        self.declare_partials('S_wet_w', 'taper')
        self.declare_partials('S_wet_w', 't_c')
        self.declare_partials('S_wet_w', 't_c_ratio')

    def compute(self, inputs, outputs):
        d_f = inputs['d_f']
        l_f = inputs['l_f']
        ln_lf = inputs['ln_lf']
        fuselage_finesse_ratio = inputs['fuselage_finesse_ratio']

        S_w = inputs['S_w']
        taper = inputs['taper']  
        t_c = inputs['t_c']   
        t_c_ratio = inputs['t_c_ratio']    

        outputs['S_wet_f'] = np.pi * d_f * l_f * (0.5 + 0.135*ln_lf)**(2/3) * (1.015+0.3/(fuselage_finesse_ratio**1.5))
        outputs['S_wet_w'] = 2 * S_w * (1 + 0.25 * t_c * ( (1 + t_c_ratio * taper) /(1 + taper) ))

    def compute_partials(self, inputs, partials):
        d_f = inputs['d_f']
        l_f = inputs['l_f']
        ln_lf = inputs['ln_lf']
        fuselage_finesse_ratio = inputs['fuselage_finesse_ratio']

        S_w = inputs['S_w']
        taper = inputs['taper']  
        t_c = inputs['t_c']   
        t_c_ratio = inputs['t_c_ratio']

        partials['S_wet_f', 'd_f'] = np.pi * l_f * (0.5 + 0.135*ln_lf)**(2/3) * (1.015+0.3/(fuselage_finesse_ratio**1.5))
        partials['S_wet_f', 'l_f'] = np.pi * d_f * (0.5 + 0.135*ln_lf)**(2/3) * (1.015+0.3/(fuselage_finesse_ratio**1.5))
        partials['S_wet_f', 'ln_lf'] = 0.282743 * d_f * l_f * (1.015 + 0.3/(fuselage_finesse_ratio**1.5)) * (0.135*ln_lf + 0.5)**(-1/3)
        partials['S_wet_f', 'fuselage_finesse_ratio'] = -1.41372 * d_f * l_f * (0.135*ln_lf+0.5)**(2/3) * (fuselage_finesse_ratio)**(-2.5)

        partials['S_wet_w', 'S_w'] = 2 * (1 + 0.25*t_c * (1 + t_c_ratio*taper)/(1+taper) )

        partials['S_wet_w', 'taper'] = 0.5 *S_w * t_c * (t_c_ratio - 1) / (taper + 1)**2
        
        partials['S_wet_w', 't_c'] = 0.5 * S_w * (t_c_ratio * taper + 1) / (taper + 1)
        partials['S_wet_w', 't_c_ratio'] =  0.5 * S_w * taper * t_c / (taper + 1)

# runs a test to see if calculated values make sense
if __name__ == "__main__":
    
    model = om.Group()
    ivc = om.IndepVarComp()
    model.add_subsystem('wetted_area_group', SWet())



    prob = Problem(model)
    prob.setup(check=True)
    # prob['wetted_area_group.speed'] = .


    prob.run_model()
    prob.model.list_inputs(prom_name=True)
    prob.model.list_outputs(prom_name=True)
  
#  ..........................work in progress.........................................


