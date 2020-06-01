

import numpy as np
from openmdao.api import Problem, Group, IndepVarComp, ExecComp, ScipyOptimizeDriver
from wingWeight import wingWeightComp


prob = Problem()

model = Group()

comp = IndepVarComp()
comp.add_output('W0', val=50000)
comp.add_output('Swing', val=1000)
comp.add_design_var('W0', lower=30000)
model.add_subsystem('inputs_comp', comp, promotes=['*'])


comp = wingWeightComp(N=3.,tc=0.3,AR=9.,sweep=30.)
model.add_subsystem('wingWeight', comp, promotes=['*'])


comp = ExecComp('totalWeight = Wwing')
comp.add_objective('totalWeight', scaler=40000.) 
model.add_subsystem('total_comp', comp, promotes=['*'])


prob.model = model

prob.driver = ScipyOptimizeDriver()
prob.driver.options['optimizer'] = 'SLSQP'
prob.driver.options['tol'] = 1e-15
prob.driver.options['disp'] = True

prob.setup()
prob.run_model()
prob.run_driver()

prob.check_partials(compact_print=True)

print('wingWeight', prob['totalWeight'])
print('W0', prob['W0'])
print('Swing', prob['Swing'])

# Visualization: ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 

