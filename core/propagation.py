#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# Time-stamp: <Mon 2013-09-09 17:15 juergen>

# import sys
import numpy as np
import math
import random
import matplotlib.pyplot as plt
import scipy.stats
#from distribution import *

from pyre import *

class Propagation(object):
  """Porpagation of corrosion

  The propagation period is defined as the period that extends from the moment
  at which steel depassivation is produced and the oxide mixture, known as
  “rust”, develops progressively to the structure reaches an unacceptable
  deterioration. This period can be determined from the so-called attack
  penetration function. This attack penetration function, :math:`P_x(t)`,
  represents the loss of rebar diameter at the time :math:`t` and it can be
  later implemented in the damage functions of the structural performance.

  In a rigorous form, the attack penetration function, :math:`P_x(t)`, takes
  the expression:

  .. math:: P_x(t) = \\int_{t_i}^{t} V_{corr}(\\tau)d\\tau
     :label: eq92

  where :math:`V_{corr}(\\tau)` is the corrosion rate at the instant
  :math:`\\tau` , and :math:`t_i` the initiation period. The function thus
  gives the progress of corrosion with time as a function of the corrosion
  rate :math:`V_{corr}` [:math:`mm/yr`].

  The main difficulty regarding the modeling of the damage function
  :math:`P_x(t)` lies in the establishment of the value of :math:`V_{corr}`,
  able to represent the particular corrosion process. There are three
  possibilities of establishing :math:`V_{corr}`:
  
     1. To assume values in function only of the exposure classes (and not of the type of attack)
     2. To estimate :math:`V_{corr}`,a from direct measurements of :math:`I_{corr}` (in specimens for new structures or on-site for existing ones)
     3. To use empirical expressions based on a variable governing the process (resistivity was selected, it is a positive decision, because it also governs the Initiation period, but it might be selected other one).

  .. note::

     Here method 3 is taken by using the Gehlen and Nilsson approach!

  :Attributes:
    - environment
  """

  def __init__(self, environment):
    self.environment = environment
    self.chloride_induced_corrosion = True

    self.data = None
    self.bins = None
    self.Vcorr = None
    self.theta = 0

  def setChlorideInducedCorrosion(self,boolean):
    """Set boolean for chloride induced corrosion.

    :Args:
      - boolean (boolean):  chloride induced corrosion True or False

    :Default:
      - boolean == True
    """
    self.chloride_induced_corrosion = boolean

  def getChlorideInducedCorrosion(self):
    """Returns the boolean for chloride induced corrosion.

    :Returns:
      - boolean.  for chloride induced corrosion
    """
    return self.chloride_induced_corrosion

  def getModelUncertaintyFactor(self):
    """Returns the model uncertainty factor.

    .. note::

       Nilsson and Gehlen propose to use a constant :math:`m_o = 882` for the
       time being. The scatter then is included into the other parameters in
       the corrosion rate model. Should mo be better quantified in the near
       future, it is simple to change this constant into a stochastic
       parameter.

    :Returns:
      - int.  :math:`m_o` constant for corrosion rate versus resistivity in
        [:math:`\\mu m \\Omega m /yr`]
    """

    model_uncertainty_factor = 882
    return model_uncertainty_factor

  def getChlorideCorrosionRateFactor(self):
    """Returns the chloride corrosion rate factor.

    :Returns:
      - random variable. :math:`F_{Cl}` chloride corrosion rate factor in [-]
    """
    theta = 0
    if self.getChlorideInducedCorrosion() == False:
      chloride_corrosion_rate_factor = 1
    else:
      mu = 0.62
      sigma = 1.35
      theta = 1.09
      chloride_corrosion_rate_factor = Lognormal('FCl',mu,sigma)
    return chloride_corrosion_rate_factor,theta

  def getGalvanicFactor(self):
    """Returns the galvanic factor.

    .. note::

       Further study is needed to quantify the galvanic effect factor. This
       should be done by carefully study of the expected deterioration
       mechanism the detailing and placement of the rebars and the surrounding
       environmental condition.

    .. note::

       If the model is restricted to ordinary cases of carbonation with
       microcell corrosion, the galvanic factor is not relevant. Consequently,
       :math:`F_{Galv} = 1`.

    :Returns:
      - int. :math:`F_{Galv}` galvanic effect factor in [-]
    """
    galvanic_factor = 1
    return galvanic_factor

  def getOxygenFactor(self):
    """Returns the oxygen factor.

    .. note::

       :math:`F_{O2}` is a factor expressing the effect of availability of
       oxygen to the corrosion process. Since data is very limited a
       statistical quantification cannot be made. However, since the supply of
       oxygen usually is believed not to be a limiting factor, except in
       submerged concrete, a crude alternative could be used: :math:`F_{O2} =
       1` in all cases except when the concrete is totally submerged when
       :math:`F_{O2}` should be zero. :math:`F_{O2} = 0`

    :Returns:
      - int. :math:`F_{O2}` oxygen availability factor in [-]
    """
    oxygen_factor = 1
    return oxygen_factor

  def getStandardResistivity(self):
    """Returns the standard resistivity.

    .. note::

       At the moment only OPC-Concrete is available!

    :Returns:
      - random variable.  :math:`\\rho_o` potential electrolytical resistivity measured
        with the standard test method at an age of 28 d in [:math:`\\Omega m`]
    """

    mu = 77
    sigma = 12
    standard_resistivity = Normal('po',mu,sigma)
    return standard_resistivity

  def getAgeFactorResistivity(self):
    """Returns the age factor resistivity.

    .. note::

       At the moment only OPC-Concrete is available!

    :Returns:
      - random variable.  :math:`n` ageing factor of the resistivity in [-]
    """

    mu = 0.23
    sigma = 0.04
    age_factor_resistivity = Normal('n',mu,sigma)
    return age_factor_resistivity

  def getCuringFactor(self):
    """Returns the curing factor.

    .. note::

       The curing factor was taken as a constant due to the lack of available
       data. Further research is needed to quantify :math:`k_c`.

    :Returns:
      - int.  :math:`k_c` curing factor for curing different from the standard
        curing in [-]

    :Raises:
      - ValueError: An error occurred if the input value is not available.
    """
    curing_factor = 1
    return curing_factor

  def getTestMethodFactor(self):
    """Returns the test method factor.

    .. note::

       Simplified implemented at the moment!

    :Returns:
      - int.  :math:`k_t` test method factor if another test method is used to
        determine the potential electrolytical resistivity :math:`\\rho_o` in
        [-]
    """
    test_method_factor = 1
    return test_method_factor

  def getTemperatureFactor(self):
    """Returns the temperature factor.

    :Returns:
      - random variable. :math:`K` value of the temperature factor for the electrolytical
        resistivity in [-]
      - float. :math:`T` the temperature
    """

    T = self.environment.getTemperature()
    K = 0
    if T > 20:
      K = Normal('K',0.073,0.015)
    elif T < 20:
      K = Normal('K',0.025,0.001)

    # temperature_factor = (1+K*(T-20))**(-1)
    # return temperature_factor
    return K,T

  def getChlorideFactor(self):
    """Returns the chloride factor.

    .. note::

       Simplified implemented at the moment!

    :Returns:
      - random variable.  :math:`k_{T,Cl}` chloride factor for the electrolytical
        resistivity in [-]
    """
    if self.getChlorideInducedCorrosion() == False:
      chloride_factor = 1
    else:
      mu = 0.72
      sigma = 0.11
      chloride_factor = Normal('kRCl',mu,sigma)
    return chloride_factor

  def getHumidityFactor(self):
    """Returns the humidity factor.

    :Returns:
      - random variable.  :math:`k_{R,RH}` humidity factor for the electrolytical
        resistivity in [-]

    :Raises:
      - ValueError: An error occurred if the input value is not available.
    """

    H = self.environment.getHumidity()
    table = [[50,6.70,1.20,3.23],
             [65,2.11,1.14,2.41],
             [80,1.43,0.73,1.33],
             [95,1.07,0.14,0.00],
             [100,1.0,0.00,0.00]]
    theta = 0

    for value in table:
      if value[0] == H:
        mu = value[1]
        sigma = value[2]
        theta = value[3]
        break
      elif value == table[-1]:
        sys.exit("Error: 'humidity' value is not in the list")

    if self.environment.getShelter == 'Sheltered':
      if H == 100:
        humidity_factor = 1
      elif H == 95:
        humidity_factor = Lognormal('kRRH',mu, sigma)
      else:
        humidity_factor = Lognormal('kRRH',mu, sigma)
    else:
      mu = 0.62
      sigma = 0.33
      theta = 0.79
      humidity_factor = Lognormal('kRRH',mu, sigma)

    return humidity_factor,theta

  def getCorrosionRateData(self,analysis='DistributionAnalysis',options=None):
    """Returns data for the corrosion rate.

    Gehlen and Nilsson [ref] proposed to express the corrosion rate as:

    .. math::  V_{corr}=\\frac{m_0}{\\rho}~F_{Cl}~F_{Galv}~F_{O2}
       :label: eq910

    in which the resistivity :math:`\\rho` is determined by considering a
    potential resistivity :math:`\\rho_o` to include the effect of the
    concrete properties and to correct this potential electrolytical
    resistivity with factors for test method, age, curing and environmental
    conditions.

    .. math:: \\rho = \\rho_o~\left(\\frac{t_{Hydr}}{t_o}\\right)^n~k_t~k_c~k_{R,T}~k_{R,RH}~k_{R,Cl}
       :label: eq911

    :Args:
      - analysis (str): Performed reliability analysis e.g. 'DistributionAnalysis'
      - options (AnalysisOption): Option for the reliability analysis

    :Returns:
      - list. :math:`V_{corr}` distribution data for the corrosion rate in [:math:`mm/yr`]
    """

    mo = self.getModelUncertaintyFactor()
    FCl,tCl = self.getChlorideCorrosionRateFactor()
    FGa = self.getGalvanicFactor()
    Fox = self.getOxygenFactor()
    po = self.getStandardResistivity()
    n = self.getAgeFactorResistivity()
    kc = self.getCuringFactor()
    kt = self.getTestMethodFactor()
    kRCl = self.getChlorideFactor()
    K,T = self.getTemperatureFactor()
    kRRH,tRRH = self.getHumidityFactor()

    mov = self.getFunctionValue('mo',mo)
    FClv = self.getFunctionValue('FCl',FCl)
    tClv = self.getFunctionValue('tCl',tCl) # const/log
    FGav = self.getFunctionValue('FGa',FGa) # const
    Foxv = self.getFunctionValue('Fox',Fox) #cosnt
    pov = self.getFunctionValue('po',po) # norm
    nv = self.getFunctionValue('n',n) # norm
    kcv = self.getFunctionValue('kc',kc) # const
    ktv = self.getFunctionValue('kt',kt) # const
    kRClv = self.getFunctionValue('kRCl',kRCl) # const/norm
    Kv = self.getFunctionValue('K',K)
    Tv = self.getFunctionValue('T',T)
    kRRHv = self.getFunctionValue('kRRH',kRRH) #const/log
    tRRHv = self.getFunctionValue('tRRH',tRRH) #const/log

    if options == None:
      options = AnalysisOptions()

    # p = po*(tHydr*to**(-1))**n*kt*kc*kRT*kRRH*kRCl
    # Vcorr = mo*p**(-1)*FCl*FGa*Fox*0.001

    string = mov+','+FClv+','+tClv+','+FGav+','+Foxv+','+pov+','+nv+','+kcv+','+ktv+','+kRClv+','+Kv+','+Tv+','+kRRHv+','+tRRHv
    function = 'gfun_vcorr('+string+')'

    g = LimitStateFunction(function)

    if analysis == 'DistributionAnalysis':
      Analysis = DistributionAnalysis(options)


    self.data = Analysis.getDistributionData()
    self.bins = Analysis.getBins()
    return self.data

  def getCorrosionRate(self,analysis='DistributionAnalysis',options=None):
    """Returns the corrosion rate.

    :Args:
      - analysis (str): Performed reliability analysis e.g. 'DistributionAnalysis'
      - options (AnalysisOption): Option for the reliability analysis

    :Returns:
      - random variable. :math:`V_{corr}` the mean corrosion rate in [:math:`mm/yr`]
    """

    data = self.getCorrosionRateData(analysis,options)
    if self.chloride_induced_corrosion == True:
      shape, loc, scale = scipy.stats.lognorm.fit(data)
      p1 = np.log(scale)
      p2 = shape
      p3 = loc
      p4 = 0
      self.Vcorr = Lognormal('Vcorr',p1,p2,1)
      self.theta = p3
    else:
      loc, scale = scipy.stats.gumbel_r.fit(data)
      self.Vcorr = Gumbel('Vcorr',loc,scale)
      self.theta = 0
    return self.Vcorr, self.theta

  def getVcorr(self):
    return self.Vcorr

  def getDistributionData(self):
    return self.data

  def datCorrosionRate(self):
    dat = self.Vcorr.getMarginalDistribution()
    return dat , self.theta

  def getBins(self):
    return self.bins

  def getFunctionValue(self,name,value):
    if type(value) == int or type(value) == float:
      return str(value)
    else:
      return name

  def getPittingFactor(self):
    """Returns the pitting factor.

    .. note::

       A better model can be found in Steward 2004

    :Returns:
      - random variable.  :math:`\\alpha` the pitting factor, taking into account the
        pitting effect in case of chloride corrosion, or the partial surface
        fraction depassivated when the carbonation is not complete in [-]
    """

    mu = 9.28
    sigma = 4.04
    alpha = Normal('alpha',mu,sigma)
    return alpha