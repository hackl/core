#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# Time-stamp: <Tue 2013-09-10 10:42 juergen>

# import core library
from core import *

import sys
import pylab as plt
import time
import datetime

start_time = time.time()


# Define a main() function.
def main():

  print ''
  print 'start - SM for Carbonation'

  # Load default settings
  concrete, reinforcement, geometrie, environment, chloride, carbonation, rate, pitting, resistance = setValues()

  # Set some options (optional)
  options = AnalysisOptions()
  options.printResults(False)

  # Input of the structural age
  age = int(raw_input("Structural Age: "))
  #age = 50.0

  # Save data to file
  filename = 'dat/carbonation/prob_carbonation_'+str(age)+'.dat'

  #==============================================================
  # Input Data
  #
  print 'CALC: Input Data'
  start_delta_time = time.time()

  # val_cov = [30,75]
  val_cov = [15,25,35,45,55,65,75,85]
  prob_cov = getUniformDistribution(val_cov)

  val_she = ['Sheltered','Unsheltered']
  prob_she = getUniformDistribution(val_she)

  val_gra = [45,40,25,35]
  prob_gra = getUniformDistribution(val_gra)

  # create nodes
  nodes_inp = []
  node_cov = Node('CoverDepth')
  node_gra = Node('Grade')
  node_she = Node('Shelter')

  # set position
  node_gra.setNodePosition(250,50)
  node_she.setNodePosition(850,50)
  node_cov.setNodePosition(1450,50)

  # set color
  node_cov.setInteriorColor('ff9900')
  node_gra.setInteriorColor('c0c0c0')
  node_she.setInteriorColor('ff99cc')

  # set outcomes
  setOutcome(node_cov,val_cov,'d')
  setOutcome(node_gra,val_gra,'C')
  setOutcome(node_she,val_she,'s')

  # append to node list
  nodes_inp.append(node_cov)
  nodes_inp.append(node_gra)
  nodes_inp.append(node_she)

  # create arcs

  # set probabilities
  node_cov.setProbabilities(prob_cov)
  node_gra.setProbabilities(prob_gra)
  node_she.setProbabilities(prob_she)

  delta_time = time.time() - start_delta_time
  print 'DONE: Input Data',str(datetime.timedelta(seconds=delta_time))

  #==============================================================
  # Carbonation
  #
  print 'CALC: carbonation'
  start_delta_time = time.time()

  val_carbonation = ['n_corrosion','y_corrosion']
  prob_carbonation = []

  if os.path.isfile(filename):
    prob_carbonation = np.loadtxt(filename)
  else:

    size = len(val_cov)*len(val_gra)*len(val_she)
    i = 1

    for cov in val_cov:
      # print 'cover:', cov
      geometrie.setCover(cov)

      for gra in val_gra:
        # print 'grade:',gra
        concrete.setGrade(gra)

        for she in val_she:
          # print 'shelter:',she
          environment.setShelter(she)

          out_str = 'Step '+str(i)+' out of '+str(size)+' steps'
          sys.stdout.write("Step %d from %d steps \r" % (i, size) )
          sys.stdout.flush()

          pf = carbonation.getFailureProbability(age,options=options)
          ps = 1-pf

          prob_carbonation.append(ps)
          prob_carbonation.append(pf)

          i += 1

    np.savetxt(filename, prob_carbonation)

  # create nodes
  nodes_Ca = []
  node_carbonation = Node('Carbonation')

  # set positions
  node_carbonation.setNodePosition(1000,900)

  # set color
  node_carbonation.setInteriorColor('ffcc99')

  # set outcomes
  node_carbonation.addOutcomes(val_carbonation)

  # append to Node list
  nodes_Ca.append(node_carbonation)

  # create arcs
  arc_cov_carbonation = Arc(node_cov, node_carbonation)
  arc_gra_carbonation = Arc(node_gra, node_carbonation)
  arc_she_carbonation = Arc(node_she, node_carbonation)

  # set probabilities
  node_carbonation.setProbabilities(prob_carbonation)


  delta_time = time.time() - start_delta_time
  print 'DONE: Carbonation',str(datetime.timedelta(seconds=delta_time))

  #==============================================================
  # Network
  #
  print 'PRINT: Network'

  nodes = []
  nodes.extend(nodes_inp)
  nodes.extend(nodes_Ca)

  net = Network('SM Carbonation')
  net.addNodes(nodes)
  save_path = '~/Dropbox/core/SM_carbonation_'+str(age)+'.xdsl'
  # path = os.path.expanduser('~/Dropbox/core/SM_carbonation.xdsl')
  path = os.path.expanduser(save_path)
  net.writeFile(path)

  print 'end - SM'
  run_time = time.time() - start_time
  print str(datetime.timedelta(seconds=run_time))


  # This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()

