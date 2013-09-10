#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import os
import numpy as np
import math
import scipy.stats
import matplotlib.pyplot as plt

from chloride import Chloride
from concrete import Concrete
from environment import Environment
from geometrie import Geometrie
from propagation import Propagation

from settings import *
from pybn import *

def getUniformDistribution(values):
  round_digits = 5
  num = len(values)
  prob = []
  for i in range(num):
    prob.append(round(1*num**(-1),round_digits))
  return prob

def getDistribution(values,bin_number,Range = [None,None]):
  #bin_number = 2
  round_digits = 5
  if Range[0] == None:
    minRange = min(values)
    maxRange = max(values)
  else:
    minRange = Range[0]
    maxRange = Range[1]

  plt.clf()
  values = np.asarray(values)
  n, bins, patches = plt.hist(values, bins = bin_number, range = (minRange,maxRange),normed = True)
  width = round(bins[1]-bins[0],round_digits)
  prob = []
  for i in range(len(n)):
    prob.append(round(width*n[i],round_digits))

  values = []
  for i in range(1,len(bins)):
    values.append(round((bins[i-1]+bins[i])*0.5,round_digits))

  if sum(prob) != 1:
    difference = 1-sum(prob)
    i = 0
    for p in prob:
      if p > 0:
        i +=1
    correcture = difference*i**(-1)
    for i in range(len(prob)):
      if prob[i] > 0:
        prob[i] = prob[i]+correcture
  # if sum(prob) != 1:
  #   print 'Error: Sum of the probabilities != 1',sum(prob)

  return values, prob, width

def setOutcome(node,value,name,add=False):
  for i in range(len(value)):
    val = str(value[i]).replace('.', '_')
    if add == False:
      string = name+'_'+val
    else:
      string = name+'_'+val+'_v'+str(i)
    node.addOutcome(string)

def getMinMaxValueForTable(table):
  maxValue = []
  minValue = []
  for i in range(len(table)):
    minValue.append(min(table[i]))
    maxValue.append(max(table[i]))

  return [min(minValue),max(maxValue)]

def getPercentile(tables,trunc):
  tab = []
  perc = []
  for table in tables:
    table.sort()
    perc.append(scipy.stats.mstats.mquantiles(table,trunc))
  perc = max(perc)
  for table in tables:
    table = filter(lambda a: a < perc, table)
    tab.append(table)
  return tab

def getDistributionForTable(table,bin_number,Range = [None,None], trunc = None):
  round_digits = 5

  if trunc != None:
    table = getPercentile(table,trunc)

  if Range[0] == None:
    minValue, maxValue = getMinMaxValueForTable(table)
  else:
    minValue = Range[0]
    maxValue = Range[1]

  val = [[] for i in range(len(table))]
  prob = [[] for i in range(len(table))]
  width = [[] for i in range(len(table))]
  for i in range(len(table)):
    val[i], prob[i], width[i] = getDistribution(table[i],bin_number,[minValue,maxValue])
  val = val[0]
  width = width[0]
  pr = []

  for i in range(len(prob)):
    sum = np.sum(prob[i])
    for ii in range(len(prob[0])):
      pr.append(prob[i][ii])

  return val, pr, width

def getTableOfFailure(calc,val,prob,width):
  round_digits = 5
  table = []
  for i in range(len(val)):
    # if val[i] == val[0]:
    #   a = round(val[i] - width*.5,round_digits+1)-0.000009
    #   b = round(val[i] + width*.5,round_digits+1)
    # elif val[i] == val[-1]:
    #   a = round(val[i] - width*.5,round_digits+1)
    #   b = round(val[i] + width*.5,round_digits+1)+0.000009
    # else:
    #   a = round(val[i] - width*.5,round_digits+1)-0.000009
    #   b = round(val[i] + width*.5,round_digits+1)+0.000009

    if val[i] == val[0]:
      a = round(val[i] - width*.5,round_digits)-0.001
      b = round(val[i] + width*.5,round_digits)
    elif val[i] == val[-1]:
      a = b #round(val[i] - width*.5,round_digits)
      b = round(val[i] + width*.5,round_digits)+0.001
    else:
      a = b
      b = round(val[i] + width*.5,round_digits)#+0.000009

    tof = []
    for ii in range(len(calc)):
      value = round(calc[ii],round_digits)
      if value >= a and value < b:
        tof.append([1,a,value,b])
      else:
        tof.append([0,a,value,b])
    table.append(tof)

  countError = 0
  prob = []
  for i in range(len(table[0])):
    prob_sum = []
    prob_cont = []
    for ii in range(len(table)):
      prob_sum.append(table[ii][i][0])
      prob_cont.append(table[ii][i])
    if sum(prob_sum) != 1:
      countError +=1
      print prob_cont
    for iii in range(len(prob_sum)):
      prob.append(prob_sum[iii])
  if countError != 0:
    print 'Error: Sum of the probabilities != 1 in', countError,'cases'
  return prob

def addConstantProbability(val,prob):
  round_digits = 6
  val.append(1)
  add_prob = []
  for i in range(len(prob)):
    add_prob.append(0)
  add_prob.append(1)
  for i in range(len(prob)):
    add_prob.append(round(prob[i],round_digits))
  add_prob.append(0)
  prob = add_prob
  return val, prob
