import numpy as np

from openmdao.api import Problem, Group, IndepVarComp, ExecComp, ScipyOptimizeDriver
from lsdo_aircraft.api import Atmosphere
from thrust_comp import thrustComp
from lift_comp import liftComp


prob = Problem()

model = Group()

comp = IndepVarComp()
comp.add_output('altitude_km', val=0.0, units ='km')
comp.add_output('BPR', val=5.0)
comp.add_output('max_thrust', val=580, units='kN') #kN

# model.add_subsystem('inputs_comp', comp, promotes=['*'])

comp = thrustComp()
model.add_subsystem('thrust', comp, promotes=['*'])


comp = ExecComp('thrus = Drag')
comp.add_constraint('Drag', equals=73)
comp.add_objective('thrus', scaler=1.0)
model.add_subsystem('horiEqui_comp', comp, promotes=['*'])


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

print('thrust', prob['Drag'])
print('altitude_km', prob['altitude_km'])
print('BPR', prob['BPR'])
print('max_thrust', prob['max_thrust'])

# prob = Problem()

# model = prob.model

# ivc = model.add_subsystem('ivc', IndepVarComp(), promotes_outputs=['*'])
# ivc.add_output('altitude_km', val=0.0, units='km')
# ivc.add_output('BPR', val=5.0)
# ivc.add_output('max_thrust', val=590, units='kN')

# model.add_subsystem('atmo', subsys=Atmosphere())
# model.add_subsystem('Thrust', subsys=thrustComp())

# model.connect('altitude_km', ['atmo.altitude_km', 'Thrust.altitude_km'])
# model.connect('BPR', ['Thrust.BPR'])
# model.connect('max_thrust', ['Thrust.max_thrust'])

# model.add_subsystem('Drag', subsys=liftComp)

# model.connect('density', ['atmo.density', 'Drag.density'])
# model.connect('CL', ['Drag.CL'])
# model.connect('speed', ['Drag.speed'])

# model.add_subsystem('horiEqui',
#                     subsys=om.ExecComp('Drag = Thrust'),
#                                         Drag={'units':'kN'},
#                                         Thrust={'units':'kN'},
#                     promotes=['*'])

# prob.driver = om.ScipyOptimizeDriver()

# model.add_design_var('altitude_km', lower=10.0, upper=13.0)
# model.add_constraint('Drag', lower=73.0, upper=73.0, scaler=1.0)
# model.add_objective('Thrust', scaler=-1.0)

# #

# prob.setup()
# prob.run_model()
# prob.run_driver()
# prob.model.list_outputs()
# prob.model.list_inputs()