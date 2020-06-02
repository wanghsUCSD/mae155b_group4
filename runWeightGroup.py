import numpy as np
from openmdao.api import Problem, Group, IndepVarComp, ExecComp, ScipyOptimizeDriver
from weight_component.weightGroup import weightCompGroup

prob = Problem()

weight_group = weightCompGroup()
prob.model.add_subsystem('empty_weight_group',weight_group)

comp = IndepVarComp()
comp.add_output('W0', val=50000)
comp.add_output('WL', val=30000)
comp.add_output('Swing', val=1000)
comp.add_output('Bw',val=200)
comp.add_output('Sht',val=200)
comp.add_output('Svt',val=200)
comp.add_design_var('W0', lower=34000)
prob.model.add_subsystem('inputs_comp', comp, promotes=['*'])

prob.setup()

prob.run_model()
prob.model.list_outputs(prom_name=True)
