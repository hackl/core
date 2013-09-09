#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

class Environment(object):
  """Environment

  The degradation process of concrete is closely related with the
  environment. For example, the risk of chloride induced corrosion is higher
  than in coastal environments as in the interior of the country.

  In the model of [DuraCrete2000]_ environmental parameters are used as
  initial conditions for the degradation models. In this context, these
  parameters are more or less represented as deterministic variables, so that
  the user of the model has to decide which assumption is accurate for the
  present situation of the structure.

  :Attributes:
    - zone (str): Different zones depending on the position compared to the water level
    - shelter (str): Surface protection
    - temperature (float): Temperature
    - humidity (float): Humidity
    - exposure (str): Exposure environment (not in use)
  """
  def __init__(self):
    self.zone = None
    self.shelter = None
    self.temperature = None
    self.humidity = None
    self.exposure = None

  def setZone(self,environment):
    """Marine Environment

    Areas that are influenced by the vicinity to an ocean, including coastal
    areas, are said to have a marine environment. Within these, different
    zones depending on the position compared to the water level.

    :Zones:
      - ``'atmospheric'`` zone. The temperature and humidity conditions in this zone are normally assumed to be equal to the regional climate.
      - ``'splash'`` zone and ``'tidal'`` zone. The temperature and humidity conditions in these zones are a mix between the conditions in the atmospheric and submerged zone. The tidal actions are caused by the gravity of the moon and the range of this zone can vary from about 0.5 m to as much as 15 m.
      - ``'submerged'`` zone. The temperature and humidity conditions in this zone are equal to the conditions in the water.

    :Args:
      - environment (str): Name of the zone e.g. ``'Tidal'``
    """
    self.zone = environment

  def getZone(self):
    """Returns the environmental zone

    :Returns:
      - zone (str): Returns the name of the environmental zone
    """
    assert self.zone != None
    return self.zone

  def setShelter(self,shelter):
    """Exposure Class

    For corrosion due to carbonation DuraCrete (1999) and DuraCrete (2000b)
    have proposed three different exposure classes:

    :Class:
      - Laboratory environment (LAB) has a constant temperature and relative humidity in the air. The surface is protected against precipitation.
      - Outdoor sheltered environment (OS), where the air temperature and the relative humidity in the air changes over the year. The surface is protected against precipitation.
      - Outdoor unsheltered environment (OUS), where the air temperature and the relative humidity in the air changes over the year. The surface is not protected against precipitation.

    :Args:
      - shelter (str): Name of the class e.g. ``'Unsheltered'``
    """
    self.shelter = shelter

  def getShelter(self):
    """Returns the exposure class

    :Returns:
      - shelter (str): Returns the name of the exposure class
    """
    assert self.shelter != None
    return self.shelter

  def setTemperature(self,temperature):
    """Set a temperature value

    :Args:
      - temperature (float): Temperature value
    """
    self.temperature = temperature

  def getTemperature(self):
    """Returns the temperature

    :Returns:
      - temperature (float): Returns the temperature
    """
    assert self.temperature != None
    return self.temperature

  def setHumidity(self,humidity):
    """Set a humidity value

    :Args:
      - humidity (int): Humidity value
    """
    self.humidity = humidity

  def getHumidity(self):
    """Returns the humidity

    :Returns:
      - humidity (int): Returns the humidity
    """
    assert self.humidity != None
    return self.humidity

  def setExposure(self,exposure):
    self.exposure = exposure

  def getExposure(self):
    assert self.exposure != None
    return self.exposure