#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# Time-stamp: <Mon 2013-09-09 16:48 juergen>

import sys
import numpy as np
import math
import random
import scipy.stats as scrnd
import scipy.special as spec

from pyre import *

class Chloride(object):
  """Chloride induced onset of corrosion

  In order to cause corrosion of rebars, chlorides must penetrate the concrete
  and the chloride content at the rebar must exceed the threshold-level
  ccrit. This depends primarily upon the immediate environmental conditions
  and on the concrete-technological parameters, which influence a) the
  chloride transport and b)the chloride binding that occurs thereby. It is
  recognised that the ingress of chlorides into concrete is a complex
  interaction of physical and chemical processes, but it is also acknowledged
  that diffusion is one of the principal mechanisms beyond the near surface
  zone. Many investigators, therefore, use the diffusion theory and the error
  function equation to model chloride ingress.

  :Attributes:
    - concrete
    - geometry
    - environment
  """

  def __init__(self, concrete, geometrie, environment):
    self.environment = environment
    self.concrete = concrete
    self.geometrie = geometrie
    self.beta = None
    self.failure_probability = None

    self.critical_chloride_definition = 1 #2
    """Definitions of threshold level

    1. Definition: Critical chloride content, at which a depassivation of the steel surface and iron dissolution begins, irrespective of whether it leads to visible corrosion damage on the concrete surface.
    2. Definition: Critical chloride content, which leads to a deterioration or damage of the concrete structure.

    If the critical content refers to Definition 2, then it is obvious that,
    depending on environmental conditions, considerably higher chloride
    concentrations must be expected than when using Definition 1. Since
    corrosion damage only occurs if in addition to steel surface
    depassivation, further conditions are met which would effect a higher
    corrosion rate (e.g., sufficient oxygen and high air humidity).

    :Default:
      - critical_chloride_definition = 2

    """
  def getDiffusionCoefficient(self):
    """Return the diffusion coefficient.

    :Returns:
      - random variable.  :math:`D_o` chloride migration coefficient at
        defined compaction, curing and environmental conditions, measured at time
        to in [:math:`mm^2/yr`] - material variable

    :Raises:
      - ValueError: An error occurred if the input value is not available.
    """

    wc = self.concrete.getWCratio()
    table = [[0.40,220.92,25.41],
             [0.45,315.60,32.51],
             [0.50,473.40,43.24]]

    for value in table:
      if value[0] == wc:
        mu = value[1]
        sigma = value[2]
        break
      elif value == table[-1]:
        sys.exit("Error: 'wc' value is not in the list")

    diffusion_coefficient = Normal('Do',mu,sigma) # [mm^2/year]

    return diffusion_coefficient


  def getEnvironmentalVariable(self):
    """Returns the environmental variable.

    :Returns:
      - random variable. :math:`k_e` constant parameter which considers the influence of
        environment on :math:`D_o` in [-] - environmental variable

    :Raises:
      - ValueError: An error occurred if the input value is not available.
    """

    table = [['Submerged',35.3038,26.6444,1.325,0.223],
             ['Tidal',35.5370,38.4599,0.9224,0.155],
             ['Splash',34.6790,130.8642,0.265,0.045],
             ['Atmospheric',35.1628,52.0160,0.676,0.114]]

    for value in table:
      if value[0] == self.environment.getZone():
        mu = value[3]
        sigma = value[4]
        break
      elif value == table[-1]:
        sys.exit("Error: 'environment' value is not in the list")

    environmental_variable = Gamma('ke',mu,sigma)
    return environmental_variable

  def getExecutionVariable(self):
    """Returns the execution variable.

    :Returns:
      - random variable. :math:`k_c` constant parameter which considers the influence of
        curing on :math:`D_o` in [-] - execution variable

    :Raises:
      - ValueError: An error occurred if the input value is not available.
    """

    days = self.concrete.getCuringPeriod()
    table = [[1,1,4,1.667,1.905],
             [3,1,4,2.148,10.741],
             [28,0.4,1,4.445,2.333]]

    if days ==7:
      execution_variable = 1
      return execution_variable
    else:
      for value in table:
        if value[0] == days:
          a = value[1]
          b = value[2]
          alpha = value[3]
          beta = value[4]
          break
        elif value == table[-1]:
          sys.exit("Error: 'curing_period' value is not in the list")

    execution_variable = Beta('kc',alpha,beta,a,b,1)

    return execution_variable

  def getTestVariable(self):
    """Returns the test variable.

    :Returns:
      - random variable. :math:`k_t` constant parameter which considers the influence of
        test method on measured :math:`D_o` in [-] - test method variable
    """

    mu = 0.832
    sigma = 0.024
    test_variable = Normal('kt',mu,sigma) # [-]

    return test_variable

  def getAgeFactor(self):
    """Returns the age factor.

    :Returns:
      - random variable. :math:`n` age factor, in [-] - environmental and material variable

    :Raises:
      - ValueError: An error occurred if the input value is not available.
    """

    # # Table form ibk
    # table = [['Submerged',0,0.98,0.362,0.245,1.009,1.719],
    #          ['Tidal',0,0.98,0.588,0.147,5.800,3.870],
    #          ['Splash',0,0.98,0.362,0.245,1.009,1.719],
    #          ['Atmospheric',0,0.98,0.362,0.245,1.009,1.719]]

    table = [['Submerged',0,1,0.30,0.05],
             ['Tidal',0,1,0.37,0.07],
             ['Splash',0,1,0.37,0.07],
             ['Atmospheric',0,1,0.65,0.07]]

    for value in table:
      if value[0] == self.environment.getZone():
        a = value[1]
        b = value[2]
        mu = value[3]
        sigma = value[4]
        break
      elif value == table[-1]:
        sys.exit("Error: 'environment' value is not in the list")

    age_factor = Beta('n',mu,sigma,a,b) # [-]
    return age_factor


  def getSurfaceChlorideConcentration(self):
    """Returns the surface chloride concentration.

    :Returns:
       - random variable.  :math:`C_s` surface chloride level in
         [:math:`wt.-\\% Cl^-/binder`] environmental and material variable

    :Raises:
      - ValueError: An error occurred if the input value is not available.
    """

    wc = self.concrete.getWCratio()
    table = [['Submerged',10.348,0.714,0,0.580],
           ['Tidal',7.758,1.360,0,1.059],
           ['Splash',7.758,1.360,0,1.105],
           ['Atmospheric',2.565,0.356,0,0.405]]

    for value in table:
      if value[0] == self.environment.getZone():
        muA = value[1]
        sigmaA = value[2]
        muE = value[3]
        sigmaE = value[4]
        break
      elif value == table[-1]:
        sys.exit("Error: 'environment' value is not in the list")

    muC = (wc)*muA+muE
    sigmaC = ((wc)**2*sigmaA**2+sigmaE**2)**(.5)

    surface_chloride_concentration = Normal('Cs',muC,sigmaC) # [%b]

    return surface_chloride_concentration

  def getCriticalChlorideConcentration(self):
    """Returns the critical chloride concentration.

    :Returns:
      - random variable. :math:`C_{crit}` critical chloride content, in [:math:`wt.-\\%
        Cl^-/binder`]

    :Raises:
      - ValueError: An error occurred if the input value is not available.
    """

    wc = self.concrete.getWCratio()
    table = [[0.30,2.30,0.20,0.90,0.15],
             [0.40,2.10,0.20,0.80,0.10],
             [0.50,1.60,0.20,0.50,0.10]]
    if self.critical_chloride_definition == 1:
      mu = 0.48
      sigma = 0.15
    else:
      for value in table:
        if value[0] == wc:
          if self.environment.getHumidity() >= 100:
            mu = value[1]
            sigma = value[2]
            break
          else:
            mu = value[3]
            sigma = value[4]
            break
        elif value == table[-1]:
          sys.exit("Error: 'wc' value is not in the list")

    critical_chloride_concentration = Normal('CCR',mu,sigma) # [mm^2/year]

    return critical_chloride_concentration

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

  def getChlorideConcentration(self,depth,age):
    """Returns the chloride concentration.

    .. math::

       C(z,t)=C_s \\left(1-erf \\frac{z}{2 \\sqrt{k_e~k_t~k_c~D_o~\\left(\\frac{t_o}{t}\\right)^n~t}} \\right)

    :Args:
      - depth (int):  distance to the concrete surface in [:math:`mm`]
      - age (int):  exposure period in [:math:`yr`]

    :Returns:
      - float.  :math:`C(x,t)` chloride level at depth :math:`x` after time
        :math:`t` in [:math:`wt.-\\%Cl^-/binder`]; being equal to the critical
        chloride content if service life is considered

    .. note::

       No longer supported!
    """

    # define parameters
    Do = self.getDiffusionCoefficient() # [mm^2/year]
    ke = self.getEnvironmentalVariable() # [-]
    kc = self.getExecutionVariable() # [-]
    kt = self.getTestVariable() # [-]
    n = self.getAgeFactor() # [-]
    Cs = self.getSurfaceChlorideConcentration() # [%b]
    t = age
    z = self.getConcreteCoverDepth(depth)
    t0 = 0.078


    # calculation

    # variable = np.absolute(ke*kt*kc*Do*(t0*t**(-1))**n*t)

    # chloride_concentration = Cs*(1-math.erf(z * (2*(variable)**(0.5))**(-1)))
    sys.exit("Error: not implemented yet")
    return chloride_concentration


  def getTimeTillCorrosion(self):
    """Returns the time till corrosion.

    .. math::

       t_{Cl}= \\left(\\frac{d^2}{4~k_e~k_t~k_c~D_o~(t_o)^n}~\\left(erf^{-1}       \\left(1-\\frac{C_{crit}}{C_s}\\right) \\right)^{-2} \\right)^{\\frac{1}{1-n}}

    :Returns:
      - float  :math:`t_{Cl}` time till corrosion, in [:math:`yr`]

    .. note::

       No longer supported!
    """

    # define parameters
    Do = self.getDiffusionCoefficient() # [mm^2/year]
    ke = self.getEnvironmentalVariable() # [-]
    kc = self.getExecutionVariable() # [-]
    kt = self.getTestVariable() # [-]
    n = self.getAgeFactor() # [-]
    Cs = self.getSurfaceChlorideConcentration() # [%b]
    CCR = self.getCriticalChlorideConcentration() # [%b]
    d = self.geometrie.getConcreteCoverDepth() #[mm]
    t0 = 0.078 # [year]

    # time_till_corrosion = ((d**(2)*(4*ke*kt*kc*Do*(t0)**(n))**(-1))*(spec.erfinv(1-CCR*Cs**(-1)))**(-2))**((1-n)**(-1))
    sys.exit("Error: not implemented yet")
    return time_till_corrosion

  def getFailureProbability(self,age,analysis='FORM',options=None):
    """Returns the probability of failure.

    For the onset of corrosion, the following limit state can be considered:

    .. math:: P_f = Pr[C(d_c,t)>C_{crit}]
       :label: eqPfChlor

    Eq. :eq:`eqPfChlor` states that the probability that the chloride content
    :math:`C` at the reinforcement at the cover depth :math:`d_c` is larger
    than the critical chloride content :math:`C_{crit}` should be smaller than
    some predefined value.

    :Args:
      - age (int):  exposure period in [:math:`yr`]
      - analysis (str): Performed reliability analysis e.g. 'FORM'
      - options (AnalysisOption): Option for the reliability analysis

    :Returns:
      - float. :math:`P_f` probability of chloride induced onset of corrosion
    """

    Do = self.getDiffusionCoefficient() # [mm^2/year]
    ke = self.getEnvironmentalVariable() # [-]
    kc = self.getExecutionVariable() # [-]
    kt = self.getTestVariable() # [-]
    n = self.getAgeFactor() # [-]
    Cs = self.getSurfaceChlorideConcentration() # [%b]
    CCR = self.getCriticalChlorideConcentration() # [%b]
    # d = self.geometrie.getConcreteCoverDepth() #[mm]
    d = self.getConcreteCoverDepth(self.geometrie.getCover()) #[mm]

    if options == None:
      options = AnalysisOptions()

    if kc == 1:
      kcv ='1'
    else:
      kcv = 'kc'
    function = 'gfun_chloride(Do,ke,'+kcv+',kt,n,Cs,CCR,d,'+str(age)+')'
    g = LimitStateFunction(function)

    if analysis == 'FORM':
      Analysis = Form(options)

    self.failure_probability = Analysis.getFailure()
    self.beta = Analysis.getBeta()

    return self.failure_probability

  def getFailureProbabilityOverTime(self,trials,age):
    """Returns the probability of failure over time.

    .. note::

       This function has to be fixed!

    :Args:
      - trials (int):  amount of trials for the monte carlo simulation
      - age (int):  exposure period in [:math:`yr`]

    :Returns:
      - list  :math:`P_f(t)` probability of chloride induced onset of corrosion

    :Raises:
      - ValueError: An error occurred if the input value is not available.
    """

    sys.exit("Error: not implemented yet")

    start = 10
    step = 10
    Failure = [0]
    failure = []
    for index in range(start,age+1,step):
      Failure.append(self.getFailureProbability(trials,index))

    for index in range(1,len(Failure)):
      yfailure = round((Failure[index]-Failure[index-1]),4)
      if yfailure < 0:
        yfailure = 0
      nfailure = round(1-yfailure,4)
      failure.append([nfailure,yfailure])

    return failure
