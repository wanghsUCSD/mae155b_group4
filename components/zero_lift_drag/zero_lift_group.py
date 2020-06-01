import numpy as np

from openmdao.api import ExplicitComponent,IndepVarComp
import openmdao.api as om
from openmdao.api import Group,Problem
from lsdo_utils.api import OptionsDictionary, LinearCombinationComp, PowerCombinationComp, GeneralOperationComp, ElementwiseMinComp
from s_wet import SWet
from skin_friction_group import SkinFrictionGroup
from form_drag.form_drag_co import FormDragCo

class ZeroLiftGroup(Group):

    def initialize(self):
        self.options.declare('shape', types=tuple)
        
    def setup(self):
        shape = self.options['shape']

        skin_friction_group = SkinFrictionGroup(
            shape = shape,
        )
        self.add_subsystem('skin_friction_group', skin_friction_group, promotes=['*'])

        wetted_area_comp = SWet()
        self.add_subsystem('wetted_area_comp', wetted_area_comp, promotes=['*'])

        form_drag_comp = FormDragCo()
        self.add_subsystem('form_drag_comp', form_drag_comp, promotes=['*'])



        comp = PowerCombinationComp(
            shape=shape,
            out_name='C0_wing',
            powers_dict=dict(
                S_wet_w=1.,
                FF_wing=1.,
                area=-1.,
                interference_factor=1.,
                ),
            )
        self.add_subsystem('C0_wing_comp', comp, promotes=['*'])


# runs a test to see if calculated values make sense
if __name__ == "__main__":
    
    shape = (1,)

    prob = Problem()

    zero_lift_group = ZeroLiftGroup(
        shape = shape,
    )
    prob.model.add_subsystem('zero_lift_group', zero_lift_group)
    


    prob.setup(check=True)


    prob.run_model()
    prob.model.list_outputs()
