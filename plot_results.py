#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# Time-stamp: <Tue 2013-09-10 13:02 juergen>

# import core library
from core import *

import matplotlib2tikz

import pylab as plt
import time
import datetime

start_time = time.time()
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

  print 'start - Plots'

  #==============================================================
  # Input Data
  #
  a = 'b'
  filename = "t-05-07-b-DCM-dc"
  amount = 8
  # filename = "t-05-08-b-DCM-wc"
  # amount = 2
  # filename = "t-05-09-a-DCM-tcur"
  # amount = 4
  # filename = "t-05-10-a-DCM-ee"
  # amount = 4
  # filename = "t-05-11-b-DCM-ds"
  # amount = 3
  # filename = "t-05-12-b-DCM-RH"
  # amount = 5
  # filename = "t-05-12-b-DCM-T"
  # amount = 8
  # filename = "t-05-13-a-DCM-vc-vi-10"
  # amount = 2
  # filename = "t-05-13-a-DCM-vc-vi-20"
  # amount = 2
  # filename = "t-05-14-a-DCM-vc-hc-10"
  # amount = 2
  # filename = "t-05-14-a-DCM-vc-hc-20"
  # amount = 2
  # filename = "t-05-13-a-DCM-ic-vi-10"
  # amount = 2
  # filename = "t-05-13-a-DCM-ic-vi-20"
  # amount = 2
  # filename = "t-05-14-a-DCM-ic-hc-10"
  # amount = 2
  # filename = "t-05-14-a-DCM-ic-hc-20"
  # amount = 2
  # filename = "t-06-03-a-DCM-dc"
  # amount = 8
  # filename = "t-06-03-b-DCM-ee-2-dc"
  # amount = 8

  Data = [[]]*(2+amount)

  save_filename = filename

  load_dir = 'dat/results/'
  save_dir = 'plots/'

  if a == 'a':
    load_path = load_dir+'DCM-a.txt'
  else:
    load_path = load_dir+'DCM-b.txt'

  path = os.path.expanduser(load_path)
  data = np.loadtxt(path)

  x = []
  Ps = []
  Pf = []
  Beta = []

  for i in range(len(data)):
    x.append(data[i][0])
    ps = data[i][1]
    pf = 1-ps
    beta = -Normal.inv_cdf(pf)

    Ps.append(ps)
    Pf.append(pf)
    Beta.append(beta)

  Data[0]=x
  if a == 'c':
    Data[1]=Beta
  else:
    Data[1]=Pf

  for num in range(amount):
    load_path = load_dir+filename+'-'+str(num)+'.txt'

    path = os.path.expanduser(load_path)
    data = np.loadtxt(path)

    Ps = []
    Pf = []
    Beta = []
    for i in range(len(data)):

      ps = data[i][1]
      pf = 1-ps
      beta = -Normal.inv_cdf(pf)

      Ps.append(ps)
      Pf.append(pf)
      Beta.append(beta)
    if a == 'c':
      Data[num+2]=Beta
    else:
      Data[num+2]=Pf


  # x = [15,25,35,45,55,65,75,85]
  # plt.clf()
  # age = [10,20,30,40,50]
  # for n in age:
  #   data = []
  #   for i in range(amount):
  #     data.append(Data[i+2][n])
  #   plt.plot(x,data,linewidth = 2)


  plt.clf()
  for num in range(amount+1):
    plt.plot(Data[0],Data[num+1],linewidth = 2)

  plt.legend( ( 'ne', '0', '1','2','3','4','5','6','7'),loc = 'upper left' )
  plt.title(r'Structural Reliability')
  plt.xlabel('Time in Service')
  if a == 'a':
    plt.ylabel('Corrosion')
  elif a == 'b':
    plt.ylabel('Failure')
  else:
    plt.ylabel('Reliability Index')
  plt.grid(True)


  save_path_png = save_dir+save_filename+".png"
  save_path_tex = save_dir+save_filename+".tex"
  path_png = os.path.expanduser(save_path_png)
  path_tex = os.path.expanduser(save_path_tex)
  plt.savefig(path_png, size=(4,3))
  matplotlib2tikz.save(path_tex)


  print 'end - Plots'
  run_time = time.time() - start_time
  print str(datetime.timedelta(seconds=run_time))


  # This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()

