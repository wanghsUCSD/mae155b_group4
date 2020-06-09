import numpy as np

from openmdao.api import Problem, Group, IndepVarComp, ExecComp, ScipyOptimizeDriver
from openaerostruct.geometry.utils import generate_mesh
from components.oas_group import OASGroup
from components.breguet_range.breguet_range_comp import BregRangeCo
from components.zero_lift_drag.zero_lift_group import ZeroLiftGroup


shape = (1,)
# Create a dictionary to store options about the mesh
mesh_dict = {'num_y' : 11,
             'num_x' : 5,
             'wing_type' : 'CRM',
             'symmetry' : False,
             'num_twist_cp' : 3}

# Generate the aerodynamic mesh based on the previous dictionary
mesh, twist_cp = generate_mesh(mesh_dict)

# Create a dictionary with info and options about the aerodynamic
# lifting surface


# Create the OpenMDAO problem
prob = Problem()

model = Group()

comp = IndepVarComp()
# comp.add_output('speed', val=257.22)
comp.add_output('rnge', val=1.3e6)
comp.add_output('isp', val=10193) #dummy variable for now
prob.model.add_subsystem('inputs_comp', comp, promotes=['*'])

comp = ZeroLiftGroup(
    shape = shape
)
prob.model.add_subsystem('zero_lift_group',comp, promotes=['*'])

CD0 = 'C0'

comp = BregRangeCo()
prob.model.add_subsystem('breguet_range_comp', comp, promotes=['*'])

surface = {
            # Wing definition
            'name' : 'wing',        # name of the surface
            'symmetry' : False,     # if true, model one half of wing
                                    # reflected across the plane y = 0
            'S_ref_type' : 'wetted', # how we compute the wing area,
                                     # can be 'wetted' or 'projected'
            'fem_model_type' : 'tube',

            'twist_cp' : twist_cp,
            'mesh' : mesh,

            # Aerodynamic performance of the lifting surface at
            # an angle of attack of 0 (alpha=0).
            # These CL0 and CD0 values are added to the CL and CD
            # obtained from aerodynamic analysis of the surface to get
            # the total CL and CD.
            # These CL0 and CD0 values do not vary wrt alpha.
            'CL0' : 0.2,            # CL of the surface at alpha=0
            'CD0' : .013,            # CD of the surface at alpha=0

            # Airfoil properties for viscous drag calculation
            'k_lam' : 0.05,         # percentage of chord with laminar
                                    # flow, used for viscous drag
            't_over_c_cp' : np.array([0.14]),      # thickness over chord ratio (NACA0015)
            'c_max_t' : .303,       # chordwise location of maximum (NACA0015)
                                    # thickness
            'with_viscous' : True,  # if true, compute viscous drag
            'with_wave' : False,     # if true, compute wave drag
            }

oas_group = OASGroup(surface=surface)
prob.model.add_subsystem('oas_group', oas_group, promotes=['*'])

comp = ExecComp('LD = CL/CD')
prob.model.add_subsystem('ld_comp', comp, promotes=['*'])

prob.model.connect('aero_point_0.CL', 'CL')
prob.model.connect('aero_point_0.CD', 'CD')

# Import the Scipy Optimizer and set the driver of the problem to use
# it, which defaults to an SLSQP optimization method
# prob.driver = om.ScipyOptimizeDriver()
# prob.driver.options['tol'] = 1e-9

# recorder = om.SqliteRecorder("aero.db")
# prob.driver.add_recorder(recorder)
# prob.driver.recording_options['record_derivatives'] = True
# prob.driver.recording_options['includes'] = ['*']

# Setup problem and add design variables, constraint, and objective
#prob.model.add_design_var('wing.twist_cp', lower=-10., upper=15.)
# prob.model.add_constraint(point_name + '.wing_perf.CL', equals=0.5)
#prob.model.add_objective(point_name + '.wing_perf.CD', scaler=1e4)

# Set up and run the optimization problem
prob.setup()
# prob.check_partials(compact_print=True)
# exit()
# prob.run_driver()
prob.run_model()
prob.model.list_inputs(prom_name=True)
prob.model.list_outputs(prom_name=True)

print(prob['aero_point_0.wing_perf.CD'][0])

print(prob['aero_point_0.wing_perf.CL'][0])

print(prob['aero_point_0.CM'][1])

print('w_frac', prob['w_frac'])
print('LD', prob['LD'])