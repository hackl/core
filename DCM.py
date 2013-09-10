#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# Time-stamp: <Tue 2013-09-10 12:26 juergen>

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
  print 'start - DCM'

  # Load default settings
  concrete, reinforcement, geometrie, environment, chloride, carbonation, rate, pitting, resistance = setValues()

  # Set some options (optional)
  options = AnalysisOptions()
  options.printResults(False)
  shared = False#True
  delta = True
  fit = False#True


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

  # val_temp = [15,20,25]
  # prob_temp = [0.3334,0.3333,0.3333]
  val_temp = [-5,0,5,10,15,20,25,30]
  prob_temp = getUniformDistribution(val_temp)

  val_hum = [50,65,80,95,100]
  prob_hum = getUniformDistribution(val_hum)

  val_dia = [10,16,27]
  # prob_dia = getUniformDistribution(val_dia)
  prob_dia = [0.3334,0.3333,0.3333]

  x_inp = 220

  # create nodes
  nodes_inp = []
  node_zone = Node('Zone')
  node_wc = Node('WCratio')
  node_cov = Node('CoverDepth')
  node_cur = Node('CuringPeriod')
  node_temp = Node('Temperature')
  node_hum = Node('Humidity')
  node_dia = Node('Diameter')

  # set position
  node_wc.setNodePosition(50,50)
  node_cur.setNodePosition(50,150)
  node_zone.setNodePosition(50,250)
  node_cov.setNodePosition(50,350)
  node_temp.setNodePosition(50,950)
  node_hum.setNodePosition(50,1050)
  node_dia.setNodePosition(50,1150)

  # set color
  node_zone.setInteriorColor('ff99cc')
  node_wc.setInteriorColor('c0c0c0')
  node_cur.setInteriorColor('c0c0c0')
  node_cov.setInteriorColor('ff9900')
  node_temp.setInteriorColor('ff99cc')
  node_hum.setInteriorColor('ff99cc')
  node_dia.setInteriorColor('99ccff')

  # set outcomes
  setOutcome(node_zone,val_zone,'z')
  setOutcome(node_wc,val_wc,'wc')
  setOutcome(node_cur,val_cur,'d')
  setOutcome(node_cov,val_cov,'dc')
  setOutcome(node_temp,val_temp,'T')
  setOutcome(node_hum,val_hum,'RT')
  setOutcome(node_dia,val_dia,'d')

  # append to node list
  nodes_inp.append(node_zone)
  nodes_inp.append(node_wc)
  nodes_inp.append(node_cur)
  nodes_inp.append(node_cov)
  nodes_inp.append(node_temp)
  nodes_inp.append(node_hum)
  nodes_inp.append(node_dia)

  # create arcs

  # set probabilities
  node_zone.setProbabilities(prob_zone)
  node_wc.setProbabilities(prob_wc)
  node_cur.setProbabilities(prob_cur)
  node_cov.setProbabilities(prob_cov)
  node_temp.setProbabilities(prob_temp)
  node_hum.setProbabilities(prob_hum)
  node_dia.setProbabilities(prob_dia)

  if shared == False:
    nodes_zone = []
    # nodes_wc = []
    # nodes_cov = []
    # nodes_cur = []
    nodes_temp = []
    nodes_hum = []
    # nodes_dia = []

    for age in service_time:

      node_zone = Node('Zone_'+repDot(str(age)))
      # node_wc = Node('WCratio_'+repDot(str(age)))
      # node_cov = Node('CoverDepth_'+repDot(str(age)))
      # node_cur = Node('CuringPeriod_'+repDot(str(age)))
      node_temp = Node('Temperature_'+repDot(str(age)))
      node_hum = Node('Humidity_'+repDot(str(age)))
      # node_dia = Node('Diameter_'+repDot(str(age)))

      # set position
      # node_wc.setNodePosition(x_inp,50)
      # node_cur.setNodePosition(x_inp,150)
      node_zone.setNodePosition(x_inp,250)
      # node_cov.setNodePosition(x_inp,350)
      node_temp.setNodePosition(x_inp,950)
      node_hum.setNodePosition(x_inp,1050)
      # node_dia.setNodePosition(x_inp,1150)
      x_inp += 170

      # set color
      node_zone.setInteriorColor('ff99cc')
      # node_wc.setInteriorColor('c0c0c0')
      # node_cur.setInteriorColor('c0c0c0')
      # node_cov.setInteriorColor('ff9900')
      node_temp.setInteriorColor('ff99cc')
      node_hum.setInteriorColor('ff99cc')
      # node_dia.setInteriorColor('99ccff')

      # set outcomes
      setOutcome(node_zone,val_zone,'z')
      # setOutcome(node_wc,val_wc,'wc')
      # setOutcome(node_cur,val_cur,'d')
      # setOutcome(node_cov,val_cov,'dc')
      setOutcome(node_temp,val_temp,'T')
      setOutcome(node_hum,val_hum,'RT')
      # setOutcome(node_dia,val_dia,'d')

      # append to node list
      nodes_zone.append(node_zone)
      # nodes_wc.append(node_wc)
      # nodes_cur.append(node_cur)
      # nodes_cov.append(node_cov)
      nodes_temp.append(node_temp)
      nodes_hum.append(node_hum)
      # nodes_dia.append(node_dia)

      # set probabilities
      node_zone.setProbabilities(prob_zone)
      # node_wc.setProbabilities(prob_wc)
      # node_cur.setProbabilities(prob_cur)
      # node_cov.setProbabilities(prob_cov)
      node_temp.setProbabilities(prob_temp)
      node_hum.setProbabilities(prob_hum)
      # node_dia.setProbabilities(prob_dia)

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
      # filename_3 = 'dat/chloride/prob_chloride_'+str(age+step_age)+'.dat'

    if os.path.isfile(filename_1):
      prob_chloride = np.loadtxt(filename_1)
      if delta:
        prob_chloride_2 = np.loadtxt(filename_2)
        # prob_chloride_3 = np.loadtxt(filename_3)
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
          pf = (prob_chloride[i]-prob_chloride_2[i])#*(step_age)**(-1)
          #pf = (prob_chloride_3[i]-prob_chloride[i])*(step_age)**(-1)
          #pf = (prob_chloride_3[i]-prob_chloride_2[i])*(2*step_age)**(-1)

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
  # Corrosion
  #
  # if fit:
  #   print 'CALC: Corrosion'
  #   start_delta_time = time.time()

  #   # create nodes
  #   nodes_corr = []
  #   val_corrosion = ['n_corrosion','y_corrosion']

  #   x_corrosion = 220

  #   # Initial Node
  #   node_corrosion = Node('Corrosion_0_0')
  #   node_corrosion.setNodePosition(50,550)
  #   node_corrosion.setInteriorColor('ff854a')
  #   node_corrosion.addOutcomes(val_corrosion)
  #   arc_chloride_corrosion = Arc(nodes_Ch[0], node_corrosion)
  #   node_corrosion.setProbabilities([1.0,0.0,0.0,1.0])
  #   nodes_corr.append(node_corrosion)

  #   node_id = 1
  #   for age in service_time:
  #     prob_corrosion = []
  #     filename = 'dat/prob/chloride2/prob_chloride_'+str(age)+'.dat'
  #     filenameA = 'dat/bel/chloride/bel_chloride_'+str(age)+'.dat'
  #     filenameB = 'dat/bel/chloride/bel_chloride_'+str(age-step_age)+'.dat'

  #     prob_chloride = np.loadtxt(filename)

  #     prob_corrosionA = np.loadtxt(filenameA)
  #     prob_corrosionB = np.loadtxt(filenameB)

  #     n1 = prob_corrosionB[0]
  #     n2 = prob_corrosionA[0]

  #     x = (1-n1)*(n1*(1-n2))**(-1)

  #     prob_delta = []
  #     # if node_id > 1:
  #     for i in range(0,len(prob_chloride),2):
  #       # print i,prob_chloride[i],x,prob_chloride[i]*x
  #       ps = prob_chloride[i]*x
  #       if ps < 0:
  #         ps = 0
  #       pf = 1-ps
  #       prob_delta.append(ps)
  #       prob_delta.append(pf)

  #     prob_chloride = prob_delta

  #     prob_add1 = []
  #     for i in range(len(prob_chloride)):
  #       if i%2==0:
  #         prob_add1.append(1)
  #       else:
  #         prob_add1.append(0)

  #     prob_add = []
  #     for i in range(len(prob_chloride)):
  #       if i%2==0:
  #         prob_add.append(0)
  #       else:
  #         prob_add.append(1)

  #     prob_corrosion = np.append(prob_add1,[prob_chloride,prob_add,prob_add])

  #     # create nodes
  #     node_corrosion = Node('Corrosion_'+repDot(str(age)))

  #     # set positions
  #     node_corrosion.setNodePosition(x_corrosion,550)
  #     x_corrosion += 170

  #     # set color
  #     node_corrosion.setInteriorColor('ff854a')

  #     # set outcomes
  #     node_corrosion.addOutcomes(val_corrosion)

  #     # append to Node list
  #     nodes_corr.append(node_corrosion)

  #     # create arcs
  #     arc_corrosionA_corrosionB = Arc(nodes_corr[node_id-1], node_corrosion)
  #     arc_chloride_corrosion = Arc(nodes_Ch[node_id], node_corrosion)

  #     arc_zone_corrosion = Arc(node_zone, node_corrosion)
  #     arc_wc_corrosion = Arc(node_wc, node_corrosion)
  #     arc_cur_corrosion = Arc(node_cur, node_corrosion)
  #     arc_cov_corrosion = Arc(node_cov, node_corrosion)

  #     # set probabilities
  #     node_corrosion.setProbabilities(prob_corrosion)

  #     # increase nodes
  #     node_id += 1

  # delta_time = time.time() - start_delta_time
  # print 'DONE: Corrosion',str(datetime.timedelta(seconds=delta_time))

  #==============================================================
  # Difference
  #
  print 'CALC: Difference'
  start_delta_time = time.time()

  nodes_diff = []
  val_diff = ['n_corrosion','y_corrosion']
  x_diff = 220

  # Initial Node
  node_diff = Node('Difference_0_0')
  node_diff.setNodePosition(50,550)
  node_diff.setInteriorColor('ff854a')
  node_diff.addOutcomes(val_diff)
  nodes_diff.append(node_diff)
  arc_chloride_diff = Arc(nodes_Ch[0], node_diff)
  node_diff.setProbabilities([1.0,0.0,0.0,1.0])

  node_id = 1
  for age in service_time:
    # create nodes
    node_diff = Node('Difference_'+repDot(str(age)))

    # set positions
    node_diff.setNodePosition(x_diff,550)
    x_diff += 170

    # set color
    node_diff.setInteriorColor('ff854a')

    # set outcomes
    node_diff.addOutcomes(val_diff)

    # append to Node list
    nodes_diff.append(node_diff)

    # create arcs
    arc_chlorideA_diff = Arc(nodes_Ch[node_id-1], node_diff)
    arc_chlorideB_diff = Arc(nodes_Ch[node_id], node_diff)

    # set probabilities
    node_diff.setProbabilities([1.,0.,0.,1.,1.,0.,1.,0.])

    # increase nodes
    node_id += 1


  delta_time = time.time() - start_delta_time
  print 'DONE: Difference',str(datetime.timedelta(seconds=delta_time))

  #==============================================================
  # Difference
  #
  print 'CALC: Delta Time'
  start_delta_time = time.time()

  nodes_delta = []

  x_dT = 220

  val_dT = ['T0_0','T'+repDot(str(step_age))]

  # Initial Node
  node_dT = Node('Delta_0_0')
  node_dT.setNodePosition(50,700)
  node_dT.setInteriorColor('ccffcc')
  node_dT.addOutcomes(val_dT)
  nodes_delta.append(node_dT)
  arc_diff_dT = Arc(nodes_diff[0], node_dT)
  node_dT.setProbabilities([1.0,0.0,0.0,1.0])

  node_id = 1
  for age in service_time:

    if node_id > 1:
      val_dT.append('T'+repDot(str(age)))

    prob_dT = [1.,0.,1.,0.,0.,1.,0.,1.]
    if node_id > 1:
      prob_dT = []
      for diff in range(len(val_diff)):
        place = 0
        for dTB in range(len(val_dT)-1):
          for dTA in range(len(val_dT)):
            if diff == 0:
              if dTA == place:
                prob_dT.append(1.)
              else:
                prob_dT.append(0.)
            else:
              if dTA == 1:
                prob_dT.append(1.)
              else:
                prob_dT.append(0.)
          place += 1
          if place == 1:
            place +=1

    # create nodes
    node_dT = Node('Delta_'+repDot(str(age)))

    # set positions
    node_dT.setNodePosition(x_dT,700)
    x_dT += 170

    # set color
    node_dT.setInteriorColor('ccffcc')

    # set outcomes
    node_dT.addOutcomes(val_dT)

    # append to Node list
    nodes_delta.append(node_dT)

    # create arcs
    arc_diff_dT = Arc(nodes_diff[node_id], node_dT)
    arc_dT_dT = Arc(nodes_delta[node_id-1], node_dT)

    # set probabilities
    node_dT.setProbabilities(prob_dT)

    # increase nodes
    node_id += 1


  delta_time = time.time() - start_delta_time
  print 'DONE: Detla Time',str(datetime.timedelta(seconds=delta_time))

  #==============================================================
  # Failure
  #
  print 'CALC: Failure'
  start_delta_time = time.time()

  nodes_Pf = []
  val_failure = ['n_failure','y_failure']
  x_failure = 220
  nominalFailure = resistance.getFailureNominal(options=options)

  # Initial Node
  node_failure = Node('Failure_0_0')
  node_failure.setNodePosition(50,850)
  node_failure.setInteriorColor('cc99ff')
  node_failure.addOutcomes(val_failure)
  nodes_Pf.append(node_failure)
  node_failure.setProbabilities([1-nominalFailure,nominalFailure])

  node_id = 1
  for age in service_time:

    prob_failure = []

    filename = 'dat/failure/prob_failure_'+str(age)+'.dat'

    if os.path.isfile(filename):
      prob_failure = np.loadtxt(filename)
    else:
      list_Vcorr = []
      Vcorr = np.loadtxt('dat/propagation/distribution.dat',dtype='S100')

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

    prob_failure = np.array([])
    val_dT = nodes_delta[node_id].getOutcomes()

    for dT in val_dT:
      dT = float(dT.replace('_', '.').replace('T', ''))

      filename = 'dat/failure/prob_failure_'+str(dT)+'.dat'

      prob_dT = np.loadtxt(filename)
      prob_failure = np.append(prob_failure,prob_dT)

    # create nodes
    node_failure = Node('Failure_'+repDot(str(age)))

    # set positions
    node_failure.setNodePosition(x_failure,850)
    x_failure += 170

    # set color
    node_failure.setInteriorColor('cc99ff')

    # set outcomes
    node_failure.addOutcomes(val_failure)

    # append to Node list
    nodes_Pf.append(node_failure)

    # create arcs
    arc_dT_failure = Arc(nodes_delta[node_id],node_failure)
    arc_chloride_failure = Arc(nodes_Ch[node_id], node_failure)

    if shared == False:
      arc_temp_failure = Arc(nodes_temp[node_id-1], node_failure)
      arc_hum_failure = Arc(nodes_hum[node_id-1], node_failure)
      # arc_dia_failure = Arc(nodes_dia[node_id-1], node_failure)
      arc_dia_failure = Arc(node_dia, node_failure)
    else:
      arc_temp_failure = Arc(node_temp, node_failure)
      arc_hum_failure = Arc(node_hum, node_failure)
      arc_dia_failure = Arc(node_dia, node_failure)

    # set probabilities
    node_failure.setProbabilities(prob_failure)

    # increase nodes
    node_id += 1

  delta_time = time.time() - start_delta_time
  print 'DONE: Failure',str(datetime.timedelta(seconds=delta_time))

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
    nodes.extend(nodes_temp)
    nodes.extend(nodes_hum)
    # nodes.extend(nodes_dia)

  nodes.extend(nodes_inp)
  nodes.extend(nodes_Ch)
  nodes.extend(nodes_diff)
  nodes.extend(nodes_delta)
  nodes.extend(nodes_Pf)

  net = Network('DCM')
  net.addNodes(nodes)
  save_path = '~/Dropbox/core/DCM.xdsl'
  path = os.path.expanduser(save_path)
  net.writeFile(path)

  print 'end - DCM'
  run_time = time.time() - start_time
  print str(datetime.timedelta(seconds=run_time))


  # This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()

