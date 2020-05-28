import numpy as np

from openmdao.api import ExplicitComponent


class maingearWeightComp(ExplicitComponent):

    def initialize(self):
        self.options.declare('Nl', types=float)
        self.options.declare('Vstall', types=float)
        
    def setup(self):
        self.add_input('Wl')
        self.add_output('Wmgear')

        self.declare_partials('Wmgear', 'Wl')

    def compute(self, inputs, outputs):
        Nl = self.options['Nl']
        Vstall = self.options['Vstall']
        
        Wl = inputs['Wl']

        outputs['Wmgear'] = 0.0106 * Wl ** 0.888 * Nl ** 0.25 * 90 ** 0.4 * 8 ** 0.321 * 2 ** -0.5 * Vstall ** 0.1

    def compute_partials(self, inputs, partials):
        Nl = self.options['Nl']
        Vstall = self.options['Vstall']

        Wl = inputs['Wl']

        partials['Wmgear', 'Wl'] = 0.0106 * 0.888 * Wl ** -0.112 * Nl ** 0.25 * 90 ** 0.4 * 8 ** 0.321 * 2 ** -0.5 * Vstall ** 0.1

class nosegearWeightComp(ExplicitComponent):

    def initialize(self):
        self.options.declare('Nl', types=float)
        
    def setup(self):
        self.add_input('Wl')
        self.add_output('Wngear')

        self.declare_partials('Wngear', 'Wl')

    def compute(self, inputs, outputs):
        Nl = self.options['Nl']
        
        Wl = inputs['Wl']

        outputs['Wngear'] = 0.032 * Wl ** 0.646 * Nl ** 0.2 * 90 ** 0.5 * 2 ** 0.45

    def compute_partials(self, inputs, partials):
        Nl = self.options['Nl']
        
        Wl = inputs['Wl']

        partials['Wngear', 'Wl'] = 0.032 * 0.646 * Wl ** -0.354 * Nl ** 0.2 * 90 ** 0.5 * 2 ** 0.45

       