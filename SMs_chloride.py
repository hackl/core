#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# Time-stamp: <Tue 2013-09-10 11:38 juergen>

# import core library
from core import *

import sys
import pylab as plt
import time
import datetime

start_time = time.time()

def SingleBayesianNetwork(age):

  # Load default settings
  concrete, reinforcement, geometrie, environment, chloride, carbonation, rate, pitting, resistance = setValues()

  # Set some options (optional)
  options = AnalysisOptions()
  options.printResults(False)

  # Save data to file
  filename = 'dat/chloride/prob_chloride_'+str(age)+'.dat'

  #==============================================================
  # Input Data
  #
  print 'CALC: Input Data'
  start_delta_time = time.time()

  val_cur = [1,3,7,28]
  prob_cur = getUniformDistribution(val_cur)

  # val_cov = [30,75]
  val_cov = [15,25,35,45,55,65,75,85]
  prob_cov = getUniformDistribution(val_cov)

  val_wc = [0.4,0.5]
  prob_wc = getUniformDistribution(val_wc)

  val_zone = ['Submerged','Tidal','Splash','Atmospheric']
  prob_zone = getUniformDistribution(val_zone)

  # create nodes
  nodes_inp = []
  node_zone = Node('Zone')
  node_wc = Node('WCratio')
  node_cov = Node('CoverDepth')
  node_cur = Node('CuringPeriod')

  # set position
  node_wc.setNodePosition(50,50)
  node_cur.setNodePosition(450,50)
  node_zone.setNodePosition(650,50)
  node_cov.setNodePosition(1450,50)

  # set color
  node_zone.setInteriorColor('ff99cc')
  node_wc.setInteriorColor('c0c0c0')
  node_cur.setInteriorColor('c0c0c0')
  node_cov.setInteriorColor('ff9900')

  # set outcomes
  setOutcome(node_zone,val_zone,'z')
  setOutcome(node_wc,val_wc,'wc')
  setOutcome(node_cur,val_cur,'d')
  setOutcome(node_cov,val_cov,'dc')

  # append to node list
  nodes_inp.append(node_zone)
  nodes_inp.append(node_wc)
  nodes_inp.append(node_cur)
  nodes_inp.append(node_cov)

  # create arcs

  # set probabilities
  node_zone.setProbabilities(prob_zone)
  node_wc.setProbabilities(prob_wc)
  node_cur.setProbabilities(prob_cur)
  node_cov.setProbabilities(prob_cov)

  delta_time = time.time() - start_delta_time
  print 'DONE: Input Data',str(datetime.timedelta(seconds=delta_time))

  #==============================================================
  # Chloride
  #
  print 'CALC: Chloride'
  start_delta_time = time.time()

  val_chloride = ['n_corrosion','y_corrosion']
  prob_chloride = []

  if os.path.isfile(filename):
    prob_chloride = np.loadtxt(filename)
  else:

    size = len(val_zone)*len(val_wc)*len(val_cur)*len(val_cov)
    i = 1
    for zone in val_zone:
      # print 'zone:', zone
      environment.setZone(zone)

      for wc in val_wc:
        # print 'wc:',wc
        concrete.setWCratio(wc)

        for cur in val_cur:
          # print 'curing:',cur
          concrete.setCuringPeriod(cur)

          for cov in val_cov:
            # print 'cover:',cov
            geometrie.setCover(cov)

            out_str = 'Step '+str(i)+' out of '+str(size)+' steps'
            sys.stdout.write("Step %d from %d steps \r" % (i, size) )
            sys.stdout.flush()

            pf = chloride.getFailureProbability(age,options=options)
            ps = 1-pf

            prob_chloride.append(ps)
            prob_chloride.append(pf)

            i += 1

    np.savetxt(filename, prob_chloride)
    print ''

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
  arc_zone_chloride = Arc(node_zone, node_chloride)
  arc_wc_chloride = Arc(node_wc, node_chloride)
  arc_cur_chloride = Arc(node_cur, node_chloride)
  arc_cov_chloride = Arc(node_cov, node_chloride)

  # set probabilities
  node_chloride.setProbabilities(prob_chloride)

  delta_time = time.time() - start_delta_time
  print 'DONE: Chloride',str(datetime.timedelta(seconds=delta_time))

  #==============================================================
  # Network
  #


# Define a main() function.
def main():

  print ''

  print 'start - SMs for Chloride'

  age = 1.0
  for i in range(50):
    print '======================'
    print 'Age',age
    SingleBayesianNetwork(age)
    age += 1.0

  print 'end - SMs'
  run_time = time.time() - start_time
  print str(datetime.timedelta(seconds=run_time))


  # This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()

