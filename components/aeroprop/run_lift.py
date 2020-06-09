import numpy as np

from openmdao.api import Problem, Group, IndepVarComp, ExecComp, ScipyOptimizeDriver
from lsdo_aircraft.api import Atmosphere
from lift_comp import liftComp


prob = Problem()

model = Group()

comp = IndepVarComp()
comp.add_output('speed', val=250)
comp.add_output('density', val=1.225)
comp.add_output('Cl', val=1.0)
comp.add_design_var('density', upper=0.0)
model.add_subsystem('inputs_comp', comp, promotes=['*'])

# atmosphere_group = Atmosphere()
# # model.add_subsystem('atmosphere_group', atmosphere_group)
# model.add_subsystem('atmosphere_group', subsys=Atmosphere())


comp = liftComp()
model.add_subsystem('lift', comp, promotes=['*'])



comp = ExecComp('Weight = lift')
comp.add_objective('Weight', scaler=120000.)  #weight in kg
model.add_subsystem('vertEqui_comp', comp, promotes=['*'])



prob.model = model

prob.driver = ScipyOptimizeDriver()
prob.driver.options['optimizer'] = 'SLSQP'
prob.driver.options['tol'] = 1e-15
prob.driver.options['disp'] = True

prob.setup()
prob.run_model()
prob.run_driver()
prob.model.list_outputs()
prob.model.list_inputs()

prob.check_partials(compact_print=True)

print('lift', prob['Weight'])
print('speed', prob['speed'])
print('density', prob['density'])
print('Cl', prob['Cl'])