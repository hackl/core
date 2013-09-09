#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# Time-stamp: <Mon 2013-09-09 16:52 juergen>

import sys
import numpy as np
import math
import random
import scipy.stats as scrnd
import scipy.special as spec

from pyre import *

class Carbonation(object):
  """Carbonation induced onset of corrosion

  The deterioration model is based on the well known 1st Fick's diffusion
  law. As can be seen in equation :eq:`eq73`, the deterioration model
  considers influencing aspects such as environmental action and
  execution. This is achieved by the introduction of a diffusion reference
  number (carbonation relevant and a measurable concrete property) in addition
  to empirically determined environmental and execution factors. Additionally,
  depending on the used compliance test arrangement a so-called test method
  factor :math:`k_t` is introduced.

  .. math:: x_c = \\sqrt{\\frac{2~k_e~k_c~k_t~D_{eff}~C_s}{a}}~\\sqrt{t}~\\left(\\frac{t_o}{t}\\right)^n
     :label: eq73

  Depending on the used compliance test arrangement the effective diffusion
  coefficient and the binding capacity will be measured directly (Accelerated
  Carbonation). In this case these parameters can be grouped together under
  one term according to formula :eq:`eq74`:

  .. math:: R_{Carb}= \\frac{a}{D_{eff}}
     :label: eq74

  :Attributes:
    - concrete
    - geometry
    - environment
  """

  def __init__(self, concrete, geometrie, environment):
    self.concrete = concrete
    self.geometrie = geometrie
    self.environment = environment

    self.failure_probability = None
    self.beta = None

  def getMaterialFactor(self):
    """Return the material factor.

    :Returns:
      - random variable. :math:`R_{Carb}` effective carbonation resistance of concrete,
        taking binding into account, at defined compaction, curing and
        environmental conditions in [:math:`kgCO_2/m^3/mm^2/yr`] - material
        variable

    :Raises:
      - ValueError: An error occurred if the input value is not available.
    """

    grade = self.concrete.getGrade()
    table = [[45,0.45,25,2.23],
             [40,0.50,5,0.38],
             [25,0.55,35,1.75],
             [35,0.55,15,0.89]]

    for value in table:
      if value[0] == grade:
        mu = value[2]
        sigma = value[3]
        break
      elif value == table[-1]:
        sys.exit("Error: 'grade' value is not in the list")

    material_factor = Normal('Rcarb',mu,sigma) # [m^2/s/kgCO2/m^3]/10**(-11)

    return material_factor

  def getEnvironmentalVariable(self):
    """Returns the environmental variable.

    :Returns:
      - random variable.  :math:`k_e` constant parameter which considers the influence of
        environment on :math:`D_{eff}` (e.g. realistic moisture history at the
        concrete surface during use) in [-] - environmental variable

    :Raises:
      - ValueError: An error occurred if the input value is not available.
    """

    table = [['Sheltered',0.85,0.26],
             ['Unsheltered',0.85,0.23]]

    for value in table:
      if value[0] == self.environment.getShelter():
        mu = value[1]
        sigma = value[2]
        break
      elif value == table[-1]:
        sys.exit("Error: 'shelter' value is not in the list")

    environmental_variable= Lognormal('ke',mu,sigma) # [-]

    return environmental_variable

  def getTestVariable(self):
    """Returns the test variable.

    :Returns:
      - random variable. :math:`k_t` constant parameter which considers the influence of
        test method on :math:`D_{eff}` in [-] - test method variable
    """

    mu = 0.983
    sigma = 0.023
    test_variable = Normal('kt',mu,sigma) # [-]

    return test_variable

  def getExecutionVariable(self):
    """Returns the execution variable.

    :Returns:
      - random variable. :math:`k_c` constant parameter which considers the influence of
        execution on :math:`D_{eff}` (e.g. influence of curing) in [-] - execution
        variable

    :Raises:
      - ValueError: An error occurred if the input value is not available.
    """

    days = self.concrete.getCuringPeriod()
    table = [[1,2.52,0.84,0.46,0],
             [3,0.87,1.03,0.88,0],
             [28,1.86,1.10,0.35,1.0]]
    theta = 0
    if days ==7:
      execution_variable = 1
    else:
      for value in table:
        if value[0] == days:
          mu = value[1]
          sigma = value[2]
          a = value[3]
          b = value[4]
          break
        elif value == table[-1]:
          sys.exit("Error: 'curing_period' value is not in the list")

      if b == 0:
        theta = a
        execution_variable = Lognormal('kc',mu,sigma)
      else:
        execution_variable = Beta('kc',mu,sigma,a,b)

    return execution_variable,theta

  def getAgeFactor(self):
    """Returns the age factor.

    :Returns:
      - random variable.  :math:`n` constant parameter which considers the influence of
        meso climatic conditions (e.g. orientation and placing of structure) in
        [-] - environmental variable

    :Raises:
      - ValueError: An error occurred if the input value is not available.
    """

    table = [['Sheltered',0.850,1.290,0,0.5,0.199,0.138],
             ['Unsheltered',0.554,0.491,0,0.5,0.265,0.175]]

    for value in table:
      if value[0] == self.environment.getShelter():
        a = value[3]
        b = value[4]
        mu = value[5]
        sigma = value[6]
        break
      elif value == table[-1]:
        sys.exit("Error: 'shelter' value is not in the list")

    age_factor = Beta('n',mu,sigma,a,b)

    return age_factor

  def getSurfaceConcentration(self):
    """Returns the surface carbonation concentration.

    :Returns:
      - random variable.  :math:`C_s` concentration of the passivator at the concrete
        surface, in this case in [:math:`kgCO_2/m^3`] - environmental variable

    .. note::
       Following DuraCrete2000, this value is a constant!
    """

    mu = 0.0006
    sigma = 0.0001
    surface_concentration = Normal('Cs',mu,sigma)

    #surface_concentration = 5*10**(-4) # [kg/m^3]
    return surface_concentration

  def getConcreteCoverDepth(self,depth):
    """Returns the cover depth

    :Args:
      - depth (float): initial value for the concrete cover in [mm]

    :Returns:
      - random variable. :math:`d_c` concrete cover depth in [mm]
    """
    mu = depth
    sigma = 0.3*mu

    concrete_cover_depth = Lognormal('d',mu, sigma) # [mm]
    return concrete_cover_depth

  def getCarbonationDepth(self,age):
    """Returns the carbonation depth.

    see Eq. :eq:`eq73`

    :Args:
      - age (int):  time in service in [:math:`yr`]

    :Returns:
      - float. :math:`x_c(t)` depth of carbonation front at time :math:`t` in
        [:math:`mm`], i.e. :math:`x_c(t)`; in case of the service life
        prediction, :math:`x_c` is equal to the concrete cover depth
        :math:`d_c`

    .. note::

       No longer supported!
    """

    # define parameters
    Rcarb = self.getMaterialFactor() # [m^2/s/kgCO2/m^3]
    ke = self.getEnvironmentalVariable() # [-]
    kt = self.getTestVariable() # [-]
    kc = self.getExecutionVariable() # [-]
    n = self.getAgeFactor() # [-]
    Cs = self.getSurfaceConcentration() # [kg/m^3]
    t = age
    ti = 1

    # carbonation_depth = ((2*kc*ke*kt*Cs*(R1carb*31556926))**(0.5)*t**(0.5)*((ti*t**(-1)))**n)*1000 # [mm]
    sys.exit("Error: not implemented yet")
    return carbonation_depth

  def getFailureProbability(self,age,analysis='FORM',options=None):
    """Returns the probability of failure.

    For the onset of corrosion, the following limit state can be considered:

    .. math:: P_f = Pr[x_c(t)>d_c]
       :label: eq71

    which states that the probability that the carbonation front :math:`x`
    reaches or is larger than the reinforcement at the cover depth :math:`d_c`
    should be smaller than some predefined value.

    :Args:
      - age (int):  exposure period in [:math:`yr`]
      - analysis (str): Performed reliability analysis e.g. 'FORM'
      - options (AnalysisOption): Option for the reliability analysis

    :Returns:
      - float.  :math:`P_f` probability of carbonation induced onset of corrosion
    """

    Rcarb = self.getMaterialFactor() # [m^2/s/kgCO2/m^3]
    ke = self.getEnvironmentalVariable() # [-]
    kt = self.getTestVariable() # [-]
    kc,theta = self.getExecutionVariable() # [-]
    n = self.getAgeFactor() # [-]
    Cs = self.getSurfaceConcentration() # [kg/m^3]
    d = self.getConcreteCoverDepth(self.geometrie.getCover()) #[mm]

    if options == None:
      options = AnalysisOptions()

    if kc == 1:
      kcv ='1'
    else:
      kcv = 'kc'
    function = 'gfun_carbonation(Rcarb,ke,kt,'+kcv+','+str(theta)+',n,Cs,d,'+str(age)+')'

    g = LimitStateFunction(function)

    if analysis == 'FORM':
      Analysis = Form(options)

    self.failure_probability = Analysis.getFailure()
    self.beta = Analysis.getBeta()

    return self.failure_probability
