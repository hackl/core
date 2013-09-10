#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# Time-stamp: <Tue 2013-09-10 08:30 juergen>

import numpy as np
import math
import random
import scipy.stats as scrnd

from pyre import *

class Resistance(object):
  """Modeling Structural Reliability

  Principally, structural reliability can be expressed as a set :math:`R` of
  random variables, describing the resistance of the structure, and a set
  :math:`S` to describe the internal stress. This principle be used for any
  kind of structure and design situation. Hence, it is difficult to make
  general statements for RC structures, because of their different geometries
  and load situations. One way to take these properties into account, is to
  normalize the random variables with respect to their nominal values. This
  makes the model applicable to a wide range of design situations.

  .. math::

     X = \\frac{X}{X_{nom}}X_{nom}

  The random variable for the resistance can be taken as the strength of the
  RC structure. Likewise, can the random variable for the internal strength or
  stress be taken as the load effect (moment, shear, etc.), which is
  considered as dimensionally consistent with the resistance. Both of them can
  be used directly to formulate the limit state function. [Ellingwood1980]_

  :Attributes:
    - concrete
    - reinforcement
    - geometry
    - propagation
    - corrosion
  """

  def __init__(self,concrete,reinforcement,geometrie,propagation,corrosion):
    self.concrete = concrete
    self.reinforcement = reinforcement
    self.geometrie = geometrie
    self.propagation = propagation
    self.corrosion = corrosion
    self.uniform_capacity_length = 500
    self.delta_time = None

    self.corrosion_rate = None

    self.pt_data = None
    self.loss_data = None
    self.apit_data = None
    self.data = None
    self.bins = None

    self.R_data = None

    self.loss_of_area = None
    self.theta = 0

    self.failure_probability = None
    self.beta = None


  def setDeltaTime(self,delta_time):
    self.delta_time = delta_time

  def getDeltaTime(self):
    return self.delta_time

  def setUniformCapacityLength(self,uniform_capacity_length):
    self.uniform_capacity_length = uniform_capacity_length

  def getUniformCapacityLength(self):
    return self.uniform_capacity_length

  def getPittingFactor(self):
    d = self.reinforcement.getDiameter()
    table = [[10,5.65,0.22,5.08,1.02],
             [16,6.2,0.18,5.56,1.16],
             [27,7.1,0.17,6.55,1.07]]

    for value in table:
      if value[0] == d:
        mu = value[1]
        CoV = value[2]
        mu_o = value[3]
        alpha_o = value[4]
        break
      elif value == table[-1]:
        sys.exit("Error: 'diameter' value is not in the list")

    Lo = 100
    LU = self.getUniformCapacityLength()

    mu = mu_o+alpha_o**(-1)*math.log(LU*Lo**(-1))
    alpha = alpha_o

    pitting_factor = Gumbel('R',mu,alpha)
    return pitting_factor

  def getPitDepth(self,delta_time=None,analysis='DistributionAnalysis',options=None):
    Vcorr,theta = self.getCorrosionRate(options)
    Vcorrv = self.getFunctionValue('Vcorr',Vcorr)
    R = self.getPittingFactor()
    if delta_time == None:
      t = self.getDeltaTime()
    else:
      t = delta_time

    if options == None:
      options = AnalysisOptions()

    function = 'gfun_pt('+Vcorrv+','+str(theta)+',R,'+str(t)+')'
    g = LimitStateFunction(function)

    if analysis == 'DistributionAnalysis':
      Analysis = DistributionAnalysis(options)

    self.pt_data = Analysis.getDistributionData()

    return self.pt_data

  def getCorrosionRate(self,options):
    if self.corrosion_rate == None:
      self.corrosion_rate = self.propagation.getCorrosionRate(options=options)
    return self.corrosion_rate

  def setCorrosionRate(self,corrosion_rate,theta=0):
    self.corrosion_rate = (corrosion_rate,theta)

  def getPitArea(self,delta_time=None,analysis='DistributionAnalysis',options=None):
    Vcorr,theta = self.getCorrosionRate(options)
    Vcorrv = self.getFunctionValue('Vcorr',Vcorr)
    R = self.getPittingFactor()
    if delta_time == None:
      t = self.getDeltaTime()
    else:
      t = delta_time

    if options == None:
      options = AnalysisOptions()

    function = 'gfun_apit('+Vcorrv+','+str(theta)+',R,Do,'+str(t)+')'
    g = LimitStateFunction(function)

    if analysis == 'DistributionAnalysis':
      Analysis = DistributionAnalysis(options)

    self.apit_data = Analysis.getDistributionData()
    return self.data

  def getLossOfAreaData(self,delta_time=None,analysis='DistributionAnalysis',options=None):
    Vcorr,theta = self.getCorrosionRate(options)
    Vcorrv = self.getFunctionValue('Vcorr',Vcorr)
    R = self.getPittingFactor()
    if delta_time == None:
      t = self.getDeltaTime()
    else:
      t = delta_time

    Do = self.reinforcement.getBarDiameter()

    if options == None:
      options = AnalysisOptions()

    if self.propagation.getChlorideInducedCorrosion():
      function = 'gfun_area_loss_pitting('+Vcorrv+','+str(theta)+',R,Do,'+str(t)+')'
    else:
      function = 'gfun_area_loss_general('+Vcorrv+','+str(theta)+',R,Do,'+str(t)+')'

    g = LimitStateFunction(function)

    if analysis == 'DistributionAnalysis':
      Analysis = DistributionAnalysis(options)

    self.loss_data = Analysis.getDistributionData()


    return self.loss_data

  def getLossOfArea(self,delta_time=None,analysis='DistributionAnalysis',options=None):
    if self.loss_data == None:
      data = self.getLossOfAreaData(delta_time,analysis,options)
    else:
      data = self.loss_data

    shape, loc, scale = scipy.stats.lognorm.fit(data,floc = 0)
    p1 = np.log(scale)
    p2 = shape
    p3 = loc
    p4 = 0
    self.loss_of_area = Lognormal('Ast',p1,p2,1)
    self.theta = p3

    return self.loss_of_area

  def getFunctionValue(self,name,value):
    if type(value) == int or type(value) == float:
      return str(value)
    else:
      return name

  def getMechanicalBehaviour(self,delta_time=None,analysis='DistributionAnalysis',options=None):
    Qlimit = 0.2 #[%]

    if self.loss_data == None:
      data = self.getLossOfAreaData(delta_time,analysis,options)
    else:
      data = self.loss_data

    ductile = []
    for Qcorr in data:
      if Qcorr < Qlimit:
        ductile.append(1)

    ductile = sum(ductile)*(len(data))**(-1)
    brittle = 1-ductile
    behaviour = ductile,brittle
    return behaviour

  def getEmpiricalCoefficient(self):
    mu = 0.005
    sigma = mu*0.2
    a = 0
    b = 0.017
    #alpha, beta = BetaAlphaBeta(mu,sigma,a,b)
    empirical_coefficient = Beta('ec',mu, sigma, a, b)
    return empirical_coefficient

  def getLossOfYieldStressData(self,delta_time=None,analysis='DistributionAnalysis',options=None):
    Vcorr,theta = self.getCorrosionRate(options)
    Vcorrv = self.getFunctionValue('Vcorr',Vcorr)
    R = self.getPittingFactor()
    if delta_time == None:
      t = self.getDeltaTime()
    else:
      t = delta_time

    Do = self.reinforcement.getBarDiameter()
    ec = self.getEmpiricalCoefficient()

    if options == None:
      options = AnalysisOptions()

    if self.propagation.getChlorideInducedCorrosion():
      function = 'gfun_yield_loss_pitting('+Vcorrv+','+str(theta)+',R,Do,'+str(t)+',ec)'
    else:
      function = 'gfun_yield_loss_general('+Vcorrv+','+str(theta)+',R,Do,'+str(t)+',ec)'

    g = LimitStateFunction(function)

    if analysis == 'DistributionAnalysis':
      Analysis = DistributionAnalysis(options)

    self.yield_data = Analysis.getDistributionData()

    return self.yield_data

  def getLossOfYieldStress(self,delta_time=None,analysis='DistributionAnalysis',options=None):
    if self.yield_data == None:
      data =   self.getLossOfYieldStressData(delta_time,analysis,options)
    else:
      data = self.yield_data

    shape, loc, scale = scipy.stats.lognorm.fit(data,floc = 0)
    p1 = np.log(scale)
    p2 = shape
    p3 = loc
    p4 = 0
    self.loss_of_yield = Lognormal('fyt',p1,p2,1)
    self.theta = p3

    return self.loss_of_yield

  def getResistanceData(self,delta_time=None,analysis='DistributionAnalysis',options=None):
    """Returns data for the resistance

    :Args:
      - delta_time (float): time since corrosion has been started in [yr]
      - analysis (str): Performed reliability analysis e.g. 'DistributionAnalysis'
      - options (AnalysisOption): Option for the reliability analysis

    :Returns:
      - list. :math:`R` distribution data for the resistance
    """

    Vcorr,theta = self.corrosion.getCorrosionRate(options)
    Vcorrv = self.getFunctionValue('Vcorr',Vcorr)
    R = self.corrosion.getPittingFactor()
    if delta_time == None:
      t = self.corrosion.getDeltaTime()
    else:
      t = delta_time

    Do = self.reinforcement.getBarDiameter()

    ec = self.corrosion.getEmpiricalCoefficient()

    ME = Lognormal('ME',1,0.1)

    h = self.geometrie.getBeamHeight()*0.001
    b = self.geometrie.getBeamWidth()*0.001

    hv = self.getFunctionValue('h',h)
    bv = self.getFunctionValue('b',b)

    fc = self.concrete.getCompressiveStrength()
    fy = self.reinforcement.getYieldStrength()

    if options == None:
      options = AnalysisOptions()

    if self.propagation.getChlorideInducedCorrosion():
      function = 'gfun_resistance_pitting('+Vcorrv+','+str(theta)+',R,Do,'+str(t)+',ec,ME,'+hv+','+bv+',fc,fy,)'
    else:
      function = 'gfun_resistance_general('+Vcorrv+','+str(theta)+',R,Do,'+str(t)+',ec,ME,'+hv+','+bv+',fc,fy,)'

    g = LimitStateFunction(function)

    if analysis == 'DistributionAnalysis':
      Analysis = DistributionAnalysis(options)

    self.R_data = Analysis.getDistributionData()

    return self.R_data


  def getFailureProbability(self,delta_time=None,analysis='FORM',options=None):
    """Returns the probability of failure

    :Args:
      - delta_time (float): time since corrosion has been started in [yr]
      - analysis (str): Performed reliability analysis e.g. 'FORM'
      - options (AnalysisOption): Option for the reliability analysis

    :Returns:
      - float. :math:`p_f` probability of failure
    """

    Vcorr,theta = self.corrosion.getCorrosionRate(options)
    Vcorrv = self.getFunctionValue('Vcorr',Vcorr)
    R = self.corrosion.getPittingFactor()
    if delta_time == None:
      t = self.corrosion.getDeltaTime()
    else:
      t = delta_time

    Do = self.reinforcement.getBarDiameter()
    ec = self.corrosion.getEmpiricalCoefficient()

    ME = Lognormal('ME',1,0.1)

    h = self.geometrie.getBeamHeight()*0.001
    b = self.geometrie.getBeamWidth()*0.001

    hv = self.getFunctionValue('h',h)
    bv = self.getFunctionValue('b',b)

    fc = self.concrete.getCompressiveStrength()
    fy = self.reinforcement.getYieldStrength()

    ym = 1.4
    yQ = 1.5
    yG = 1.35

    Rk = .871435#0.829938#.83#.59#.5396#0.647
    Gk = 1
    Qk = 2.037

    a = 0.5
    z = (a*yG*Gk+(1-a)*yQ*Qk)*ym*Rk**(-1)

    Re = Lognormal('Re',1.05,1.05*0.11)
    G = Normal('G',1,0.1)
    Q = Gumbel('Q',1,0.4)

    if options == None:
      options = AnalysisOptions()

    if self.propagation.getChlorideInducedCorrosion():
      function = 'gfun_failure_pitting('+Vcorrv+','+str(theta)+',R,Do,'+str(t)+',ec,ME,'+hv+','+bv+',fc,fy,'+str(z)+','+str(a)+',Re,G,Q)'
    else:
      function = 'gfun_failure_general('+Vcorrv+','+str(theta)+',R,Do,'+str(t)+',ec,ME,'+hv+','+bv+',fc,fy,'+str(z)+','+str(a)+',Re,G,Q)'

    g = LimitStateFunction(function)

    if analysis == 'FORM':
      Analysis = Form(options)
      #Analysis = CrudeMonteCarlo(options)
    self.failure_probability = Analysis.getFailure()
    self.beta = Analysis.getBeta()
    self.corrosion_rate = None

    return self.failure_probability

  def getBeta(self):
    """Returns the beta value for the RC structure

    :Returns:
      - float. :math:`\\beta` reliability index
    """

    return self.beta

  def getFailureNominal(self,delta_time=None,analysis='FORM',options=None):
    """Returns the probability of failure without damage caused by corrosion

    :Args:
      - delta_time (float): time since corrosion has been started in [yr]
      - analysis (str): Performed reliability analysis e.g. 'FORM'
      - options (AnalysisOption): Option for the reliability analysis

    :Returns:
      - float. :math:`p_f` probability of failure without corrosion
    """

    ME = Lognormal('ME',1,0.1)

    ym = 1.4
    yQ = 1.5
    yG = 1.35

    Rk = .871435
    Gk = 1
    Qk = 2.037

    a = 0.5
    z = (a*yG*Gk+(1-a)*yQ*Qk)*ym*Rk**(-1)

    Re = Lognormal('Re',1.05,1.05*0.11)
    G = Normal('G',1,0.1)
    Q = Gumbel('Q',1,0.4)

    if options == None:
      options = AnalysisOptions()

    function = 'gfun_failure_nom(ME,'+str(z)+','+str(a)+',Re,G,Q)'
    g = LimitStateFunction(function)

    if analysis == 'FORM':
      Analysis = Form(options)
      #Analysis = CrudeMonteCarlo(options)
    self.failure_probability = Analysis.getFailure()
    self.beta = Analysis.getBeta()

    return self.failure_probability
