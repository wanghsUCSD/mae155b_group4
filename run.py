import numpy as np 

from openmdao.api import Problem, IndepVarComp

from lsdo_aircraft.api import Aircraft, AircraftGroup
from lsdo_aircraft.api import Geometry, LiftingSurfaceGeometry, BodyGeometry, PartGeometry
from lsdo_aircraft.api import Analyses

from components.zero_lift_drag.zero_lift_drag import ZeroLiftDrag

n = 1
shape = (n,)

geometry = Geometry()

geometry.add(LiftingSurfaceGeometry(
    name='wing',
    lift_coeff_zero_alpha=0.23,
))
geometry.add(LiftingSurfaceGeometry(
    name='tail',
    dynamic_pressure_ratio=0.9,
))
geometry.add(BodyGeometry(
    name='fuselage',
    fuselage_aspect_ratio=10.,
))
geometry.add(PartGeometry(
    name='balance',
    parasite_drag_coeff=0.006,
))

analyses = Analyses()

aircraft = Aircraft(
    geometry=geometry,
    analyses=analyses,
    aircraft_type='transport',
)


prob = Problem()

comp = IndepVarComp()
comp.add_output('altitude', val=11000., shape=shape)
comp.add_output('speed', val=250., shape=shape)
comp.add_output('alpha', val=3. * np.pi / 180., shape=shape)
comp.add_output('ref_area', val=427.8, shape=shape)
comp.add_output('ref_mac', val=7., shape=shape)

prob.model.add_subsystem('inputs_comp', comp, promotes=['*'])


aircraft_group = AircraftGroup(shape=shape, aircraft=aircraft)
prob.model.add_subsystem('aircraft_group', aircraft_group, promotes=['*'])

zero_lift_group = ZeroLiftDrag(shape=shape,aircraft=aircraft)
prob.model.add_subsystem('zero_lift_group', zero_lift_group, promotes=['*'])

prob.setup(check=True)

prob.run_model()
prob.model.list_outputs(prom_name=True)
prob.model.list_inputs()