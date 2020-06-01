from openmdao.api import Group
from openmdao.api import IndepVarComp

from weight_component.wingWeight import wingWeightComp
from weight_component.tailWeight import htailWeightComp
from weight_component.tailWeight import vtailWeightComp
from weight_component.fuselageWeight import fuselageWeightComp
from weight_component.gearWeight import maingearWeightComp
from weight_component.gearWeight import nosegearWeightComp
from weight_component.hydraulicWeight import hydraulicWeightComp
from weight_component.airconWeight import airconWeightComp

class weightCompGroup(Group):


    def setup(self):
        comp = wingWeightComp(N=3.,tc=0.3,AR=9.,sweep=30.)
        self.add_subsystem('wingWeight',comp,promotes=['*'])

        comp = htailWeightComp(N=3.,Lt=85.,ARht=4.,sweepht=27.)
        self.add_subsystem('htailWeight',comp,promotes=['*'])

        comp = vtailWeightComp(N=3.,Lt=85.,ARvt=4.,sweepvt=27.,tc=0.3)
        self.add_subsystem('vtailWeight',comp,promotes=['*'])

        comp = fuselageWeightComp(N=3.,L=205.,LD=17.,Sfuse=15030.,sweep=30.,taper=0.3)
        self.add_subsystem('fuselageWeight',comp,promotes=['*'])

        comp = maingearWeightComp(Nl=5.,Vstall=150.)
        self.add_subsystem('maingearWeight',comp,promotes=['*'])

        comp = nosegearWeightComp(Nl=5.)
        self.add_subsystem('nosegearWeight',comp,promotes=['*'])

        comp = airconWeightComp(Np=410.,Vpr=39000.)
        self.add_subsystem('airconWeight',comp,promotes=['*'])

        comp = hydraulicWeightComp()
        self.add_subsystem('hydraulicWeight',comp,promotes=['*'])
