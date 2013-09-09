#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

from pyre import *

class Concrete(object):
  """ Concrete

  Concrete is a composite material made of aggregates and reaction products of
  cement and mixing water.

  :Attributes:
    - name (str): Name of the concrete e.g. 'C25/30'
    - water_cement_ratio (float): water-cement ratio of the concrete
    - curing period (int): curring period of the concrete
    - grade (int): grade of the concrete
  """

  def __init__(self, name):
    self.name = name
    self.water_cement_ratio = None
    self.curing_period = None
    self.grade = None

  def setWCratio(self, wcRatio):
    """ Set a wc-ratio

    :Args:
      - wcRatio (float): water-cement ratio of the concrete
    """
    self.water_cement_ratio = wcRatio

  def getWCratio(self):
    """Returns the wc-ratio

    :Returns:
      - water_cement_ratio (float): Returns the water-cement ratio 
    """
    assert self.water_cement_ratio != None
    return self.water_cement_ratio

  def setCuringPeriod(self, period):
    """ Set the curing period for the concrete

    :Args:
      - curing_period (int): Curing period in days
    """
    self.curing_period = period

  def getCuringPeriod(self):
    """Returns the curing period for the concrete

    :Returns:
      - curing_period (int): Returns the curing period in days
    """

    assert self.curing_period != None
    return self.curing_period

  def setGrade(self, grade):
    """ Set the concrete grade

    :Args:
      - grade (float): Grade of the concrete
    """
    self.grade = grade

  def getGrade(self):
    """Returns the concrete grade

    :Returns:
      - grade (float): Returns the grade of the concrete
    """

    assert self.grade != None
    return self.grade

  def getCompressiveStrength(self):
    """Returns the compressive strength

    :Returns:
      - compressive_strength (float): Returns fc of the concrete
    """

    # mu = 33
    # sigma = 5
    # compressive_strength = Normal('fc',mu,sigma)

    mu = 30
    sigma = 5
    compressive_strength = Lognormal('fc',mu,sigma)

    return compressive_strength

  def __str__(self):
    return self.name

