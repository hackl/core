#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# Time-stamp: <Tue 2013-09-10 10:43 juergen>

# import core library
from core import *

import os
import sys
import pylab as plt
import scipy.stats
import warnings

# just for suppressing warnings
warnings.simplefilter('ignore')

import time
import datetime

start_time = time.time()


# Define a main() function.
def main():

  print ''
  print 'start - SM for Propagation'

  # Load default settings
  concrete, reinforcement, geometrie, environment, chloride, carbonation, rate, pitting, resistance = setValues()

  # Set some options (optional)
  options = AnalysisOptions()
  options.printResults(False)
  # options.setSamples(2000)
  N = options.getBins()

  # Save data to file
  filename_1 = 'dat/propagation/propagation.dat'
  filename_2 = 'dat/propagation/distribution.dat'

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

  # create nodes
  nodes_inp = []
  node_temp = Node('Temperature')
  node_hum = Node('Humidity')

  # set position
  node_temp.setNodePosition(1050,50)
  node_hum.setNodePosition(1250,50)

  # set color
  node_temp.setInteriorColor('ff99cc')
  node_hum.setInteriorColor('ff99cc')

  # set outcomes
  setOutcome(node_temp,val_temp,'T')
  setOutcome(node_hum,val_hum,'RT')

  # append to node list
  nodes_inp.append(node_temp)
  nodes_inp.append(node_hum)

  # create arcs

  # set probabilities
  node_temp.setProbabilities(prob_temp)
  node_hum.setProbabilities(prob_hum)

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
  print 'CALC: Propagation'
  start_delta_time = time.time()
  size_Vcorr = len(val_temp)*len(val_hum)*len(val_chloride)
  dist_Vcorr = []

  if os.path.isfile(filename_1):
    Vcorr = np.loadtxt(filename_1)
  else:
    Vcorr = [None for i in range(size_Vcorr)]

    i = 0
    size = len(val_chloride)*len(val_temp)*len(val_hum)
    j = 1
    for chloride in val_chloride:
      if chloride == 'n_corrosion':
        rate.setChlorideInducedCorrosion(False)
      else:
        rate.setChlorideInducedCorrosion(True)

      for temp in val_temp:
        environment.setTemperature(temp)

        for hum in val_hum:
          environment.setHumidity(hum)

          out_str = 'Step '+str(j)+' out of '+str(size)+' steps'
          sys.stdout.write("Step %d from %d steps \r" % (j, size) )
          sys.stdout.flush()

          corrosion_rate = rate.getCorrosionRate(options=options)
          dat_Vcorr,theta_Vcorr = rate.datCorrosionRate()
          data_Vcorr = rate.getDistributionData()
          lis = []
          for dat in dat_Vcorr:
            lis.append(dat)
          lis.append(theta_Vcorr)
          lis.append(chloride)
          lis.append(temp)
          lis.append(hum)
          dist_Vcorr.append(lis)

          # # Print histogram and fitting function
          # filename_3 = 'plots/Vcorr/Vcorr_sa_'+str(i)+'.png'
          # print filename_3

          # maxx = np.max(data_Vcorr)
          # minx = np.min(data_Vcorr)
          # x = np.linspace(minx,maxx,500)
          # plt.clf()
          # plt.hist(data_Vcorr,N,  normed=True, facecolor='green', alpha=0.75,label='Vcorr')

          # if chloride == 'y_corrosion':
          #   a,b,c = scipy.stats.lognorm.fit(data_Vcorr)
          #   f = scipy.stats.lognorm.pdf(x,a,b,c)
          #   plt.plot(x,f,'b-',label = 'Lognormal')
          # else:
          #   a,b = scipy.stats.gumbel_r.fit(data_Vcorr)
          #   f = scipy.stats.gumbel_r.pdf(x,a,b)
          #   plt.plot(x,f,'b-',label = 'Gumbel')

          # plt.title('Distribution Analysis for Vcorr')
          # plt.xlabel('Corrosion Rate [mm/yr]')
          # plt.ylabel('Probability Density [-]')
          # plt.legend()
          # plt.savefig(filename_3, size=(4,3))

          Vcorr[i] = data_Vcorr
          i += 1
          j += 1

    np.savetxt(filename_1, Vcorr)
    np.savetxt(filename_2, dist_Vcorr, fmt='%s')

  Vcorr = np.asarray(Vcorr)
  val_Vcorr, prob_Vcorr, width_Vcorr = getDistributionForTable(Vcorr,N,trunc=0.95)

  # create nodes
  nodes_Pr = []
  node_Vcorr =  Node('CorrosionRate')

  # set positions
  node_Vcorr.setNodePosition(1600,900)

  # set color
  node_Vcorr.setInteriorColor('ccffcc')

  # set size
  node_Vcorr.setNodeSize(180,65)

  # set outcomes
  setOutcome(node_Vcorr,val_Vcorr,'Vcorr')

  # append to Node list
  nodes_Pr.append(node_Vcorr)

  # create arcs
  arc_chloride_Vcorr = Arc(node_chloride, node_Vcorr)
  arc_temp_Vcorr = Arc(node_temp, node_Vcorr)
  arc_hum_Vcorr = Arc(node_hum, node_Vcorr)

  # set probabilities
  node_Vcorr.setProbabilities(prob_Vcorr)

  delta_time = time.time() - start_delta_time
  print 'DONE: Propagation',str(datetime.timedelta(seconds=delta_time))

  #==============================================================
  # Network
  #
  # print 'PRINT: Network'

  nodes = []
  nodes.extend(nodes_inp)
  nodes.extend(nodes_Ch)
  nodes.extend(nodes_Pr)

  net = Network('SM Propagation')
  net.addNodes(nodes)
  path = os.path.expanduser('~/Dropbox/core/SM_propagation.xdsl')
  net.writeFile(path)

  print 'end - SM'
  run_time = time.time() - start_time
  print str(datetime.timedelta(seconds=run_time))


  # This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()

