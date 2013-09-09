#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# Time-stamp: <Mon 2013-09-09 18:24 juergen>

import numpy as np
import math
import random
import scipy.stats as scrnd

from pyre import *

class Pitting(object):
  """Pitting corrosion

  Local or pitting corrosion is only associated with chloride induced
  corrosion. The area of the anode (active zone) may be relative small, but
  once corrosion has been initiated the resulting electrical field attracts
  negative chloride ions towards the pit. Hence, the corrosion rate can be
  relative high which leads to an extreme loss of steel cross
  section. [LIFECON2003]_

  The [DuraCrete2000]_ model provides only a very simplified model for the
  effects of pitting corrosion. For this reason, a hemispherical model of a
  pit, suggested by Val and Melchers (1997) and modified by Stewart (2004,
  2009, 2012), is used in this context.

  :Attributes:
    - reinforcement
    - propagation
  """

  def __init__(self, reinforcement,propagation):
    self.reinforcement = reinforcement
    self.propagation = propagation
    self.uniform_capacity_length = 500
    self.delta_time = None

    self.corrosion_rate = None

    self.pt_data = None
    self.loss_data = None
    self.apit_data = None
    self.data = None
    self.bins = None

    self.loss_of_area = None
    self.theta = 0

  def setDeltaTime(self,delta_time):
    """Set the time since corrosion has been started

    :Args:
      - delta_time (float): time since corrosion has been started in [yr]
    """
    self.delta_time = delta_time

  def getDeltaTime(self):
    """Return time since corrosion has been started

    :Returns:
      - float. :math:`t_{corr}` time since corrosion has been stated
    """
    return self.delta_time

  def setUniformCapacityLength(self,uniform_capacity_length):
    """Set uniform capacity length

    :Args:
      - uniform_capacity_length (int): uniform capacity length in [mm]
    """
    self.uniform_capacity_length = uniform_capacity_length

  def getUniformCapacityLength(self):
    """Returns the uniform capacity length

    :Returns:
      - int. :math:`L_U` is the uniform capacity length, referring to the
        distance along a structural member in which pitting corrosion will
        have a detrimental effect on structural capacity. 
    """
    return self.uniform_capacity_length

  def getPittingFactor(self):
    """Returns the pitting factor

    According to [Gonzalez1995]_ is the corrosion rate for pitting corrosion
    four to eight times higher than the average penetration on the surface of
    a reinforcement bar.

    :Returns:
      - random variable. :math:`R_{pitt}` is  the ratio between maximum and
        average corrosion penetration and is called pitting factor

    :Raises:
      - ValueError: An error occurred if the input value is not available.
    """

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
    """Returns data for the pit depth

    For simplicity, a hemispherical form of pits is assumed. The radius of the
    pit, :math:`p_{max}`, at time :math:`t`, can be estimated as

    .. math::

       p_{max} (t) = V_{corr} t_{corr} R_{pit}

    :Args:
      - delta_time (float): time since corrosion has been started in [yr]
      - analysis (str): Performed reliability analysis e.g. 'DistributionAnalysis'
      - options (AnalysisOption): Option for the reliability analysis

    :Returns:
      - list. :math:`p_{max}` distribution data for the pit depth in [mm]
    """

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
    """Returns data for the pit area

    The pit configuration is used to predict the cross sectional area of the
    pit, denoted by :math:`A_{pit}`.

    :Args:
      - delta_time (float): time since corrosion has been started in [yr]
      - analysis (str): Performed reliability analysis e.g. 'DistributionAnalysis'
      - options (AnalysisOption): Option for the reliability analysis

    :Returns:
      - list. :math:`A_{pit}(t)` distribution data for the pit area in [:math:`mm^2`]
    """

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
    return self.apit_data

  def getLossOfAreaData(self,delta_time=None,analysis='DistributionAnalysis',options=None):
    """Returns data for the area loss caused by corrosion 

    .. math::

       A_s(t) = A_{s,nom} − A_{pit}(t)

    :Args:
      - delta_time (float): time since corrosion has been started in [yr]
      - analysis (str): Performed reliability analysis e.g. 'DistributionAnalysis'
      - options (AnalysisOption): Option for the reliability analysis

    :Returns:
      - list. :math:`A_{s}(t)` distribution data for steal area in [:math:`mm^2`]
    """

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
    """Returns a random variable the area loss caused by corrosion

    .. math::

       A_s(t) = A_{s,nom} − A_{pit}(t)

    :Args:
      - delta_time (float): time since corrosion has been started in [yr]
      - analysis (str): Performed reliability analysis e.g. 'DistributionAnalysis'
      - options (AnalysisOption): Option for the reliability analysis

    :Returns:
      - random variable. :math:`A_{s}(t)` distribution for the steal area in [:math:`mm^2`]
    """

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
    """Returns the mechanical behavior of the reinforcement bar

    :Args:
      - delta_time (float): time since corrosion has been started in [yr]
      - analysis (str): Performed reliability analysis e.g. 'DistributionAnalysis'
      - options (AnalysisOption): Option for the reliability analysis

    :Returns:
      - tuple. :math:`(p_{ductile},p_{brittle})` percentage for ductile or brittle behavior
    """

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
    """Returns the empirical coefficient

    :Returns:
      - random variable. :math:`ec` empirical coefficient for the mechanical behavior

    """
    mu = 0.005
    sigma = mu*0.2
    a = 0
    b = 0.017
    #alpha, beta = BetaAlphaBeta(mu,sigma,a,b)
    empirical_coefficient = Beta('ec',mu, sigma, a, b)
    return empirical_coefficient

  def getLossOfYieldStressData(self,delta_time=None,analysis='DistributionAnalysis',options=None):
    """Returns data for the loss of yield strength caused by corrosion 

    .. math::

       f_y(t) = (1 − ec Q_{corr}(t)) f_{y,o}

    :Args:
      - delta_time (float): time since corrosion has been started in [yr]
      - analysis (str): Performed reliability analysis e.g. 'DistributionAnalysis'
      - options (AnalysisOption): Option for the reliability analysis

    :Returns:
      - list. :math:`f_{y}(t)` distribution data for yield strength in [:math:`N/mm^2`]
    """

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
    """Returns a random variable for the loss of yield strength caused by corrosion

    :Args:
      - delta_time (float): time since corrosion has been started in [yr]
      - analysis (str): Performed reliability analysis e.g. 'DistributionAnalysis'
      - options (AnalysisOption): Option for the reliability analysis

    :Returns:
      - random variable. :math:`f_{y}(t)` distribution for the yield strength in [:math:`N/mm^2`]
    """

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
