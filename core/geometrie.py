#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import random

class Geometrie(object):
  """Geometry

  :Attributes:
    - name (str): Name of the Structure e.g. 'Beam'
    - concrete_cover (float): Concrete cover depth
    - beam_width (float): width of a beam
    - beam_height (float): height of a beam
    - beam_length (float): length of a beam
  """
  def __init__(self, name):
    self.name = name
    self.concrete_cover = None
    self.beam_width = None
    self.beam_height = None
    self.beam_length = None

  def setCover(self, cover):
    """Set the initial concrete cover depth

    In addition the thickness of the concrete cover denoted by :math:`d_c` ,
    is an important parameter for the RC structure. Beside the effect to bond
    the reinforcement to the concrete, the cover protects steel bars against
    corrosion.

    :Args:
      - cover (float): Initial concrete cover in [mm]
    """
    self.concrete_cover = cover

  def getCover(self):
    """Returns the initial concrete cover depth

    :Returns:
      - concrete_cover (float): Returns the initial concrete cover
    """
    assert self.concrete_cover != None
    return self.concrete_cover

  def getConcreteCoverDepth(self):
    """Returns the concrete cover depth

    :Returns:
      - concrete_cover_depth (float): Returns a random value for the concrete cover
    """
    assert self.concrete_cover != None
    mu = self.concrete_cover
    sigma = 0.3*mu
    lamda, zita = LogNormLamdaZita(mu,sigma)

    concrete_cover_depth = random.lognormvariate(lamda, zita) # [mm]
    return concrete_cover_depth

  def setBeamWidth(self,width):
    """Set a width for the beam

    :Args:
      - width (float): beam width in [mm]
    """
    self.beam_width = width

  def getBeamWidth(self):
    """Returns the width of the beam

    :Returns:
      - beam_width (float): Returns the beam width
    """
    assert self.beam_width != None
    return self.beam_width

  def setBeamHeight(self,height):
    """Set a height for the beam

    :Args:
      - height (float): beam height in [mm]
    """
    self.beam_height = height

  def getBeamHeight(self):
    """Returns the height of the beam

    :Returns:
      - beam_height (float): Returns the beam height
    """
    assert self.beam_height != None
    return self.beam_height

  def getBeamDepth(self):
    """Returns depth of the beam

    :Returns:
      - beam_depth (float): Returns beam depth :math:`d = h-d_c`
    """
    beam_depth = self.getBeamHeight()-self.getConcreteCoverDepth()
    return beam_depth


  def setBeamLength(self,length):
    """Set the length of the beam

    :Args:
      - length (float): beam length in [mm]
    """
    self.beam_length = length

  def getBeamLength(self):
    """Returns the length of the beam

    :Returns:
      - beam_length (float): Returns the beam length
    """
    assert self.beam_length != None
    return self.beam_length

  def __str__(self):
    return self.name
