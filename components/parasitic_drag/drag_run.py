import numpy as np

from openmdao.api import ExplicitComponent, Problem, Group, IndepVarComp

from form_drag_co import FormDragCo
from wave_drag_co import WaveDragCo

prob = Problem()

model = Group()

comp = FormDragCo()

prob.model = model

prob.setup()
prob.run_model()

print('FF_wing', prob['FF_wing'])
print('FF_fuselage', prob['FF_fuselage'])
print('FF_nacelle', prob['FF_nacelle'])
