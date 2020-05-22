import numpy as np

from openmdao.api import ExplicitComponent, Problem, Group, IndepVarComp

from breguet_range_comp import BregRangeCo 

prob = Problem()

model = Group()

comp = BregRangeCo()
model.add_subsystem('breg_range_comp', comp, promotes=['*'])

prob.model = model

prob.setup()
prob.run_model()

print('w_frac', prob['w_frac'])


