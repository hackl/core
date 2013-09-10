#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# Time-stamp: <Tue 2013-09-10 12:14 juergen>

# import core library
from core import *

import sys
import pylab as plt
import time
import datetime

start_time = time.time()

def repDot(string):
  return string.replace('.', '_')

def drange(start, stop, step):
  values = []
  r = start
  while r < stop:
    values.append(r)
    r += step
  return values

# Define a main() function.
def main():

  print ''
  print 'start - DBN for Chloride'

  # Load default settings
  concrete, reinforcement, geometrie, environment, chloride, carbonation, rate, pitting, resistance = setValues()

  # Set some options (optional)
  options = AnalysisOptions()
  options.printResults(False)
  shared = False#True
  delta = True

  # Structural age
  start_age = 0
  end_age = 50
  step_age = 1.

  service_time = drange(start_age+step_age,end_age+step_age,step_age)

  # print service_time

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

  x_inp = 220

  # create nodes
  nodes_inp = []
  node_zone = Node('Zone')
  node_wc = Node('WCratio')
  node_cov = Node('CoverDepth')
  node_cur = Node('CuringPeriod')

  # set position
  node_wc.setNodePosition(50,50)
  node_cur.setNodePosition(50,150)
  node_zone.setNodePosition(50,250)
  node_cov.setNodePosition(50,350)

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

  if shared == False:
    nodes_zone = []
    # nodes_wc = []
    # nodes_cov = []
    # nodes_cur = []
    for age in service_time:

      node_zone = Node('Zone_'+repDot(str(age)))
      # node_wc = Node('WCratio_'+repDot(str(age)))
      # node_cov = Node('CoverDepth_'+repDot(str(age)))
      # node_cur = Node('CuringPeriod_'+repDot(str(age)))

      # set position
      # node_wc.setNodePosition(x_inp,50)
      # node_cur.setNodePosition(x_inp,150)
      node_zone.setNodePosition(x_inp,250)
      # node_cov.setNodePosition(x_inp,350)
      x_inp += 170

      # set color
      node_zone.setInteriorColor('ff99cc')
      # node_wc.setInteriorColor('c0c0c0')
      # node_cur.setInteriorColor('c0c0c0')
      # node_cov.setInteriorColor('ff9900')

      # set outcomes
      setOutcome(node_zone,val_zone,'z')
      # setOutcome(node_wc,val_wc,'wc')
      # setOutcome(node_cur,val_cur,'d')
      # setOutcome(node_cov,val_cov,'dc')

      # append to node list
      nodes_zone.append(node_zone)
      # nodes_wc.append(node_wc)
      # nodes_cur.append(node_cur)
      # nodes_cov.append(node_cov)

      # set probabilities
      node_zone.setProbabilities(prob_zone)
      # node_wc.setProbabilities(prob_wc)
      # node_cur.setProbabilities(prob_cur)
      # node_cov.setProbabilities(prob_cov)

  delta_time = time.time() - start_delta_time
  print 'DONE: Input Data',str(datetime.timedelta(seconds=delta_time))

  #==============================================================
  # Chloride
  #
  print 'CALC: Chloride'
  start_delta_time = time.time()

  nodes_Ch = []
  val_chloride = ['n_corrosion','y_corrosion']
  x_chloride = 220

  # Initial Node
  node_chloride = Node('Chloride_0_0')
  node_chloride.setNodePosition(50,450)
  node_chloride.setInteriorColor('ffff99')
  node_chloride.addOutcomes(val_chloride)
  nodes_Ch.append(node_chloride)
  node_chloride.setProbabilities([1.0,0.0])

  node_id = 1
  for age in service_time:
    prob_chloride = []
    filename_1 = 'dat/chloride/prob_chloride_'+str(age)+'.dat'
    if delta:
      filename_2 = 'dat/chloride/prob_chloride_'+str(age-step_age)+'.dat'
      # filename_3 = 'dat/prob/chloride/prob_chloride_'+str(age+step_age)+'.dat'

    if os.path.isfile(filename_1):
      prob_chloride = np.loadtxt(filename_1)
      if delta:
        prob_chloride_2 = np.loadtxt(filename_2)
        #prob_chloride_3 = np.loadtxt(filename_3)
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

      np.savetxt(filename_1, prob_chloride)

    # = Delta -Start ===============
    if delta:
      prob_delta = []
      if node_id > 1:
        for i in range(1,len(prob_chloride),2):
          # pf = prob_chloride[i]
          pf = (prob_chloride[i]-prob_chloride_2[i])#*(step_age)**(-1)
          #pf = (prob_chloride_3[i]-prob_chloride[i])#*(step_age)**(-1)
          #pf = (prob_chloride_3[i]-prob_chloride_2[i])#*(2*step_age)**(-1)

          if pf < 0:
            pf = 0
          ps = 1-pf
          prob_delta.append(ps)
          prob_delta.append(pf)

        prob_chloride = prob_delta

      prob_add = []
      for i in range(len(prob_chloride)):
        if i%2==0:
          prob_add.append(0)
        else:
          prob_add.append(1)

      prob_chloride = np.append(prob_chloride,prob_add)

    # = Delta - End ================


    # create nodes
    node_chloride = Node('Chloride_'+repDot(str(age)))

    # set positions
    node_chloride.setNodePosition(x_chloride,450)
    x_chloride += 170

    # set color
    node_chloride.setInteriorColor('ffff99')

    # set outcomes
    node_chloride.addOutcomes(val_chloride)

    # append to Node list
    nodes_Ch.append(node_chloride)

    # create arcs
    if delta:
      arc_chlorideA_chlorideB = Arc(nodes_Ch[node_id-1], node_chloride)
    if shared == False:
      arc_zone_chloride = Arc(nodes_zone[node_id-1], node_chloride)
      # arc_wc_chloride = Arc(nodes_wc[node_id-1], node_chloride)
      # arc_cur_chloride = Arc(nodes_cur[node_id-1], node_chloride)
      # arc_cov_chloride = Arc(nodes_cov[node_id-1], node_chloride)
      arc_wc_chloride = Arc(node_wc, node_chloride)
      arc_cur_chloride = Arc(node_cur, node_chloride)
      arc_cov_chloride = Arc(node_cov, node_chloride)
    else:
      arc_zone_chloride = Arc(node_zone, node_chloride)
      arc_wc_chloride = Arc(node_wc, node_chloride)
      arc_cur_chloride = Arc(node_cur, node_chloride)
      arc_cov_chloride = Arc(node_cov, node_chloride)

    # set probabilities
    node_chloride.setProbabilities(prob_chloride)

    # increase nodes
    node_id += 1

  delta_time = time.time() - start_delta_time
  print 'DONE: Chloride',str(datetime.timedelta(seconds=delta_time))

  #==============================================================
  # Network
  #
  print 'PRINT: Network'

  nodes = []
  if shared == False:
    nodes.extend(nodes_zone)
    # nodes.extend(nodes_wc)
    # nodes.extend(nodes_cov)
    # nodes.extend(nodes_cur)
  nodes.extend(nodes_inp)
  nodes.extend(nodes_Ch)

  net = Network('DBN Chloride')
  net.addNodes(nodes)
  save_path = '~/Dropbox/core/DNB_chloride.xdsl'
  path = os.path.expanduser(save_path)
  net.writeFile(path)

  print 'end - DBN'
  run_time = time.time() - start_time
  print str(datetime.timedelta(seconds=run_time))


  # This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()

