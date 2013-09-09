#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

# import pyre library
from core import *

import matplotlib.pyplot as plt
# from settings import *

import time
import datetime
start_time = time.time()


# Define a main() function.
def main():
  # Load default settings
  concrete, reinforcement, geometrie, environment, chloride, carbonation, rate, pitting, resistance = setValues()

  # Define random variables
  # Do = Normal('Do',220.92,25.41)
  # ke = Gamma('ke',0.9224,0.155)
  # kc = Beta('kc',1.667,1.905,1,4,1)
  # kt = Normal('kt',0.832,0.024)
  # n = Beta('n',0.37,0.07,0,1)
  # Cs = Normal('Cs',3.103,1.191)
  # CCR = Normal('CCR',0.80,0.10)
  # d = Lognormal('d',30,22.5)

  # If the random variables are correlatet, then define a correlation matrix,
  # else no correlatin matrix is needed
  # Corr = CorrelationMatrix([[1.0, 0.3, 0.2],
#                            [0.3, 1.0, 0.2],
#                            [0.2, 0.2, 1.0]])

  # Define limit state function
  # - case 1: define directly
  # g = LimitStateFunction('1 - X2*(1000*X3)**(-1) - (X1*(200*X3)**(-1))**2')
#  g = LimitStateFunction('X1*X2-X3')
  # - case 2: define load function, wich is defined in function.py
#  g = LimitStateFunction('function(Do,ke,kc=1,kt,n,Cs,CCR,d,t=50)')

 

  # Set some options (optional)
  options = AnalysisOptions()
  options.printResults(False)
  age = 50
  #geometrie.setCover(10)
  
  print chloride.getFailureProbability(age,options=options)

  B = []
  x = range(10,101,10)
  for i in x:
    geometrie.setCover(i)
    pf = chloride.getFailureProbability(age,options=options)
    # Analysis = CrudeMonteCarlo(options)
    print 'Pf at depth',i,'is',pf
    B.append(pf)

  plt.clf()
  plt.plot(x,B, label='Pf_chloride_50_depth')
  plt.legend(loc="best")
  plt.savefig("Pf_chloride_depth.png", size=(4,3))

  # B = []
  # x = range(10,101,10)
  # for i in x:
  #   string = 'gfun_chloride(Do,ke,kc,kt,n,Cs,CCR,d,t='+str(i)+')'
  #   g = LimitStateFunction(string)
  #   Analysis = Form(options)
  #   # Analysis = CrudeMonteCarlo(options)
  #   print 'Pf at age',i,'is',Analysis.getFailure()
  #   B.append(Analysis.getFailure())

  # plt.clf()
  # plt.plot(x,B, label='Pf_chloride_FORM')
  # plt.legend(loc="best")
  # plt.savefig("Pf.png", size=(4,3))

  
  # Performe FORM analysis
  # Analysis = Form(options)

  # Performe Crude Monte Carlo Simulation
  #Analysis = CrudeMonteCarlo(options)

  # Some single results:
  # beta = Analysis.getBeta()
  # failure = Analysis.getFailure()

  run_time = time.time() - start_time
  print str(datetime.timedelta(seconds=run_time))


  # This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()

