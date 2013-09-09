#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import math
from pyre import *

class Reinforcement(object):
  """Reinforcement

  Because of the low tensile strength of concrete, it is reinforced with steel
  bars or wires that resist the tensile stresses.

  :Attributes:
    - name (str): Name of the steal e.g. 'S500'
    - yield_strength (float): yield strength of the steal
    - diameter (float): Diameter of the steal bar
    - bars (int): Amount on reinforcement
  """

  def __init__(self, name):
    self.name = name
    self.yield_stress = None
    self.diameter = None
    self.bars = None

  def setYieldStress(self, yield_stress):
    """ Define a yield strength for the steal

    :Args:
      - yield_stress (float): yield stress for the reinforcement
    """
    self.yield_stress = yield_stress

  def getYieldStress(self):
    """Returns the yield strength

    :Returns:
      - yield_stress (float): Returns the yield strength of the reinforcement bar
    """
    assert self.yield_stress != None
    return self.yield_stress

  def setDiameter(self, diameter):
    """ Set an initial diameter

    :Args:
      - diameter (float): initial diameter of the reinforcement bar
    """
    self.diameter = diameter

  def getDiameter(self):
    """Returns the initial diameter

    :Returns:
      - diameter (float): Returns the initial diameter
    """
    assert self.diameter != None
    return self.diameter

  def getBarDiameter(self):
    """Returns the bar diameter

    :Returns:
      - bar_diameter (random): Returns the bar diameter as a random variable
    """
    assert self.diameter != None
    mu = self.diameter
    sigma = mu*0.01
    bar_diameter = Normal('Do',mu,sigma)
    return bar_diameter

  def setBars(self, bars):
    """ Set amount of reinforcement bars

    :Args:
      - bars (int): Amount of reinforcement bars
    """
    self.bars = bars

  def getBars(self):
    """Returns the amount of reinforcement bars

    :Returns:
      - bars (int): Returns the amount of reinforcement bars
    """
    assert self.bars != None
    return self.bars

  def getNominalBarArea(self):
    """Returns the cross-section area of the reinforcement bar

    :Returns:
      - bar_area (random): Returns a random variable for the cross-section area
    """
    d = self.getDiameter()
    mu = math.pi*4**(-1)*d**2
    sigma = mu*0.02
    bar_area = random.gauss(mu,sigma)
    return bar_area

  def getYieldStrength(self):
    """Returns the yield strength

    :Returns:
      - yield strength (random): Returns the yield strength as a random variable
    """
    # mu = 560
    # sigma = 37 #30
    # yield_strength = Normal('fy',mu,sigma)

    # JCSS
    mu = 560
    sigma = 30 #30
    yield_strength = Lognormal('fy',mu,sigma)

    return yield_strength

  def __str__(self):
    return self.name