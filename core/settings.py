#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

from concrete import Concrete
from reinforcement import Reinforcement
from geometrie import Geometrie
from environment import Environment
from chloride import Chloride
from carbonation import Carbonation
from propagation import Propagation
from corrosion import Pitting
from resistance import Resistance

def setValues():
  """Default settings

  :Returns:
    - Default settings for the probabilistic models for degradation of concrete.
  """

  # Concrete settings
  concrete = Concrete('C25/30')

  concrete.setWCratio(0.4)
  # values: (0.3),0.4,(0.45),0.5

  concrete.setCuringPeriod(1)
  # values: 1,3,7,28

  concrete.setGrade(45)
  # values: 45,40,25,35

  # Reinforcement settings
  reinforcement = Reinforcement('S500')
  reinforcement.setYieldStress(500)
  # values: all

  reinforcement.setDiameter(16)
  # values: (8),10,16,27

  reinforcement.setBars(1)
  # values: all

  # Geometry settings
  geometrie = Geometrie('Beam')
  geometrie.setCover(30) # values: all
  geometrie.setBeamWidth(350)
  geometrie.setBeamHeight(550)
  geometrie.setBeamLength(5000)

  # Environment settings
  environment = Environment()

  environment.setZone('Submerged')
  # values: 'Submerged','Tidal','Splash','Atmospheric'

  environment.setHumidity(80)
  # values: 50,65,80,95,100

  # for the simplified corrosion rate:
  # environment.setExposure('Wet-Dry')
  # values: 'Wet','Wet-Dry','Airborne sea water','Tidal'

  environment.setTemperature(20)
  # values: all

  environment.setShelter('Unsheltered')
  # 'Sheltered','Unsheltered'

  # Chloride
  chloride = Chloride(concrete,geometrie,environment)

  # Carbonation
  carbonation = Carbonation(concrete,geometrie,environment)

  # Propagation
  rate = Propagation(environment)

  # Corrosion
  pitting = Pitting(reinforcement,rate)
  # pitting.setDeltaTime(50)
  # values: all

  # Resistance
  resistance = Resistance(concrete,reinforcement,geometrie,rate,pitting)

  return concrete, reinforcement, geometrie, environment, chloride, carbonation, rate, pitting, resistance
