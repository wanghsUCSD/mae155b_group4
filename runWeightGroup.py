import numpy as np
from openmdao.api import Problem, Group, IndepVarComp, ExecComp, ScipyOptimizeDriver
from weight_component.weightGroup import weightCompGroup

prob = Problem()

weight_group = weightCompGroup()
prob.model.add_subsystem('empty_weight_group',weight_group)

prob.setup()

prob.run_model()
prob.model.list_outputs(prom_name=True)
