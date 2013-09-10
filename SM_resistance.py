#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# Time-stamp: <Tue 2013-09-10 11:21 juergen>

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


# Define a main() function.
def main():

  print ''

  print 'start - SM for Resistance'

  # Load default settings
  concrete, reinforcement, geometrie, environment, chloride, carbonation, rate, pitting, resistance = setValues()

  # Set some options (optional)
  options = AnalysisOptions()
  options.printResults(False)
  options.setSamples(1000)
  N = options.getBins()

  # Input of the structural age
  age = int(raw_input("Structural Age: "))
  #age = 50.0

  # Load data from file
  filename_a = 'dat/propagation/distribution.dat'

  # Save data to file
  filename_1 = 'dat/resistance/resistance.dat'

  #==============================================================
  # Input Data
  #
  print 'CALC: Input Data'
  start_delta_time = time.time()

  val_temp = [15,20,25]
  prob_temp = [0.3334,0.3333,0.3333]
  # prob_temp = getUniformDistribution(val_temp)

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
  # Propagation
  #

  # Some calculations
  # ...

  #==============================================================
  # Corrosion
  #
  print 'CALC: Resistance'
  start_delta_time = time.time()

  size_loss = len(val_temp)*len(val_hum)*len(val_chloride)*len(val_dia)
  Mu = [None for i in range(size_loss)]

  if os.path.isfile(filename_1):
    Mu = np.loadtxt(filename_1)
  else:
    Mu = [None for i in range(size_loss)]

    list_Vcorr = []
    Vcorr = np.loadtxt(filename_a,dtype='S100')

    i = 0
    j = 0
    size = len(val_temp)*len(val_hum)*len(val_chloride)*len(val_dia)
    k = 1
    for temp in val_temp:
      # print 'temp',temp

      environment.setTemperature(temp)
      for hum in val_hum:
        # print 'hum', hum
        environment.setHumidity(hum)

        for chloride in val_chloride:
          # print 'chloride',chloride
          if chloride == 'n_corrosion':
            rate.setChlorideInducedCorrosion(False)
          else:
            rate.setChlorideInducedCorrosion(True)

          for dia in val_dia:
            # print 'dia',dia

            distributionType = getDistributionType(int(Vcorr[i][0]))
            VcorrD = eval(distributionType+"('Vcorr',"+Vcorr[i][1]+","+Vcorr[i][2]+")")
            thetaD = float(Vcorr[i][8])

            resistance.setCorrosionRate(VcorrD,thetaD)
            reinforcement.setDiameter(dia)

            out_str = 'Step '+str(k)+' out of '+str(size)+' steps'
            sys.stdout.write("Step %d from %d steps \r" % (k, size) )
            sys.stdout.flush()

            data = resistance.getResistanceData(age,options=options)

            # # Print histogram and fitting function
            # filename_3 = 'plots/R/R_'+str(j)+'.png'
            # print filename

            # maxx = np.max(data)
            # minx = np.min(data)
            # x = np.linspace(minx,maxx,500)

            # plt.clf()
            # plt.hist(data,N,  normed=True, facecolor='green', alpha=0.75,label='R')

            # a,b = scipy.stats.norm.fit(data)
            # f = scipy.stats.norm.pdf(x,a,b)
            # plt.plot(x,f,'b-',label = 'Normal')

            # plt.title('Distribution Analysis for Mu')
            # plt.xlabel('Random Values')
            # plt.ylabel('Probability Density')
            # plt.legend()
            # plt.savefig(filename_3, size=(4,3))

            Mu[j] = data

            VcorrD = []
            thetaD = []
            j +=1
            k +=1
          i += 1
    np.savetxt(filename_1, Mu)

  # val_Aloss, prob_Aloss, width_Aloss = getDistributionForTable(Aloss,100,Range = [0,1])
  val_Mu, prob_Mu, width_Mu = getDistributionForTable(Mu,N)

  # create nodes
  nodes_R = []
  node_Mu =  Node('Resistance')

  # set positions
  node_Mu.setNodePosition(2900,900)

  # set color
  node_Mu.setInteriorColor('cc99ff')

  # set outcomes
  setOutcome(node_Mu,val_Mu,'Mu')

  # append to Node list
  nodes_R.append(node_Mu)

  # create arcs
  arc_temp_Mu = Arc(node_temp, node_Mu)
  arc_hum_Mu = Arc(node_hum, node_Mu)
  arc_chloride_Mu = Arc(node_chloride, node_Mu)
  arc_dia_Mu = Arc(node_dia, node_Mu)

  # set probabilities
  node_Mu.setProbabilities(prob_Mu)

  delta_time = time.time() - start_delta_time
  print 'DONE: Resistance',str(datetime.timedelta(seconds=delta_time))

  #==============================================================
  # Network
  #
  print 'PRINT: Network'

  nodes = []
  nodes.extend(nodes_inp)
  nodes.extend(nodes_Ch)
  nodes.extend(nodes_R)

  net = Network('SM Resistance')
  net.addNodes(nodes)
  path = os.path.expanduser('~/Dropbox/core/SM_resistance.xdsl')
  net.writeFile(path)

  print 'end - SM'
  run_time = time.time() - start_time
  print str(datetime.timedelta(seconds=run_time))


  # This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()

