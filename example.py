#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

# import core library
from core import *

import matplotlib.pyplot as plt
import time
import datetime

start_time = time.time()


# Define a main() function.
def main():
  # Load default settings
  concrete, reinforcement, geometrie, environment, chloride, carbonation, rate, pitting, resistance = setValues()

  # Set some analysis options (optional)
  options = AnalysisOptions()
  options.printResults(False)
  age = 50

  # Calculate the probability of failure after 50 years and the default settings
  pf = chloride.getFailureProbability(age,options=options)
  print 'Pf after ',age,'years is',pf
  print ''

  # Calculate the probability of failure after 50 years by different concrete covers
  B = []
  x = range(10,101,10)
  for i in x:
    geometrie.setCover(i)
    pf = chloride.getFailureProbability(age,options=options)
    # Analysis = CrudeMonteCarlo(options)
    print 'Pf at depth',i,'is',pf
    B.append(pf)

  # save the results from the analysis as a plot
  plt.clf()
  plt.plot(x,B, label='Probability of Failure by different cover depths')
  plt.legend(loc="best")
  plt.savefig("Pf_chloride_depth.png", size=(4,3))

  run_time = time.time() - start_time
  print str(datetime.timedelta(seconds=run_time))


  # This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()

