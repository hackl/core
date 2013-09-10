#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# Time-stamp: <Tue 2013-09-10 11:46 juergen>

# import core library
from core import *

import os
import sys

import pylab as plt
import scipy.stats
import warnings

# just for surpressing warnings
warnings.simplefilter('ignore')

import time
import datetime

start_time = time.time()

def SingleBayesianNetwork(age):

  # Load default settings
  concrete, reinforcement, geometrie, environment, chloride, carbonation, rate, pitting, resistance = setValues()

  # Set some options (optional)
  options = AnalysisOptions()
  options.printResults(False)
  options.setSamples(1000)
  N = options.getBins()

  # Load data from file
  filename_a = 'dat/propagation/distribution.dat'

  # Save data to file
  filename = 'dat/failure/prob_failure_'+str(age)+'.dat'

  #==============================================================
  # Input Data
  #
  print 'CALC: Input Data'
  start_delta_time = time.time()

  # val_temp = [15,20,25]
  # prob_temp = [0.3334,0.3333,0.3333]
  val_temp = [-5,0,5,10,15,20,25,30]
  prob_temp = getUniformDistribution(val_temp)

  val_hum = [50,65,80,95,100]
  prob_hum = getUniformDistribution(val_hum)

  val_dia = [10,16,27]
  # prob_dia = getUniformDistribution(val_dia)
  prob_dia = [0.3334,0.3333,0.3333]

  # create nodes
  nodes_inp = []
  node_temp = Node('Temperature')
  node_hum = Node('Humidity')
  node_dia = Node('Diameter')

  # set position
  node_temp.setNodePosition(1050,50)
  node_hum.setNodePosition(1250,50)
  node_dia.setNodePosition(1650,50)

  # set color
  node_temp.setInteriorColor('ff99cc')
  node_hum.setInteriorColor('ff99cc')
  node_dia.setInteriorColor('99ccff')

  # set outcomes
  setOutcome(node_temp,val_temp,'T')
  setOutcome(node_hum,val_hum,'RT')
  setOutcome(node_dia,val_dia,'d')

  # append to node list
  nodes_inp.append(node_temp)
  nodes_inp.append(node_hum)
  nodes_inp.append(node_dia)

  # create arcs

  # set probabilities
  node_temp.setProbabilities(prob_temp)
  node_hum.setProbabilities(prob_hum)
  node_dia.setProbabilities(prob_dia)

  delta_time = time.time() - start_delta_time
  print 'DONE: Input Data',str(datetime.timedelta(seconds=delta_time))

  #==============================================================
  # Chloride
  #
  print 'CALC: Chloride'
  start_delta_time = time.time()

  val_chloride = ['n_corrosion','y_corrosion']
  prob_chloride = [0.6,0.4]

  # Some calculations
  # ...

  # create nodes
  nodes_Ch = []
  node_chloride = Node('Chloride')

  # set positions
  node_chloride.setNodePosition(100,300)

  # set color
  node_chloride.setInteriorColor('ffff99')

  # set outcomes
  node_chloride.addOutcomes(val_chloride)

  # append to Node list
  nodes_Ch.append(node_chloride)

  # create arcs

  # set probabilities
  node_chloride.setProbabilities(prob_chloride)

  delta_time = time.time() - start_delta_time
  print 'DONE: Chloride',str(datetime.timedelta(seconds=delta_time))

  #==============================================================
  # Failure
  #
  print 'CALC: Failure'
  start_delta_time = time.time()

  val_failure = ['n_failure','y_failure']
  prob_failure = []

  nominalFailure = resistance.getFailureNominal(options=options)

  if os.path.isfile(filename):
    prob_failure = np.loadtxt(filename)
  else:

    list_Vcorr = []
    Vcorr = np.loadtxt(filename_a,dtype='S100')

    i = 0
    j = 0
    size = len(val_chloride)*len(val_temp)*len(val_hum)*len(val_dia)
    k = 1
    for chloride in val_chloride:
      # print 'chloride',chloride
      if chloride == 'n_corrosion':
        rate.setChlorideInducedCorrosion(False)
      else:
        rate.setChlorideInducedCorrosion(True)

      for temp in val_temp:
        # print 'temp',temp
        environment.setTemperature(temp)

        for hum in val_hum:
          # print 'hum', hum
          environment.setHumidity(hum)

          for dia in val_dia:
            # print 'dia',dia

            out_str = 'Step '+str(k)+' out of '+str(size)+' steps'
            sys.stdout.write("Step %d from %d steps \r" % (k, size) )
            sys.stdout.flush()
            k += 1

            distributionType = getDistributionType(int(Vcorr[i][0]))
            VcorrD = eval(distributionType+"('Vcorr',"+Vcorr[i][1]+","+Vcorr[i][2]+")")
            thetaD = float(Vcorr[i][8])

            resistance.setCorrosionRate(VcorrD,thetaD)
            reinforcement.setDiameter(dia)

            if chloride == 'n_corrosion' or age == 0.0:
              pf = nominalFailure
            else:
              pf = resistance.getFailureProbability(age,options=options)
            ps = 1-pf

            prob_failure.append(ps)
            prob_failure.append(pf)

            j +=1
          i += 1
    np.savetxt(filename,prob_failure)
    print ''

  # create nodes
  nodes_Pf = []
  node_failure = Node('Failure')

  # set positions
  node_failure.setNodePosition(2900,900)

  # set color
  node_failure.setInteriorColor('cc99ff')

  # set outcomes
  node_failure.addOutcomes(val_failure)

  # append to Node list
  nodes_Pf.append(node_failure)

  # create arcs
  arc_chloride_failure = Arc(node_chloride, node_failure)
  arc_temp_failure = Arc(node_temp, node_failure)
  arc_hum_failure = Arc(node_hum, node_failure)
  arc_dia_failure = Arc(node_dia, node_failure)

  # set probabilities
  node_failure.setProbabilities(prob_failure)

  delta_time = time.time() - start_delta_time
  print 'DONE: Failure',str(datetime.timedelta(seconds=delta_time))

  #==============================================================
  # Network
  #
  # print 'PRINT: Network'

  # nodes = []
  # nodes.extend(nodes_inp)
  # nodes.extend(nodes_Ch)
  # nodes.extend(nodes_Pf)

  # net = Network('SM Failure')
  # net.addNodes(nodes)
  # path = os.path.expanduser('~/Dropbox/core/SMs_failure.xdsl')
  # net.writeFile(path)

# Define a main() function.
def main():

  print ''
  print 'start - SMs for Failure'

  # SingleBayesianNetwork(1.)
  age = 0.25
  age = 0.
  for i in range(51):
    print '======================'
    print 'Age',age
    SingleBayesianNetwork(age)
    age += 1.

  print 'end - SMs'
  run_time = time.time() - start_time
  print str(datetime.timedelta(seconds=run_time))


  # This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
