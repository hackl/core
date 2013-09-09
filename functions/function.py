#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import numpy as np
import math
import scipy.special as spec

def function(X1,X2,X3):
  g = 1 - X2*(1000*X3)**(-1) - (X1*(200*X3)**(-1))**2
  return g

def gfun_chloride(Do,ke,kc,kt,n,Cs,CCR,d,t):

  t0 = 0.078
#  kc = 1
  root = np.absolute(ke*kt*kc*Do*(t0*t**(-1))**n*t)
  chloride_concentration = Cs*(1-spec.erf(d * (2*(root)**(0.5))**(-1)))
  
#  chloride_concentration = Cs*(1-spec.erf(d * (2*(ke*kt*kc*Do*(t0*t**(-1))**n*t)**(0.5))**(-1)))

  g = CCR - chloride_concentration
  return g






def gfun_carbonation(Rcarb,ke,kt,kc,theta,n,Cs,d,t):
  Rcarb = Rcarb*10**(-11)
  kc = kc+theta
  ti = 1
  carbonation_depth = ((2*kc*ke*kt*Cs*(Rcarb*31556926))**(0.5)*t**(0.5)*((ti*t**(-1)))**n)*1000

  g = d - carbonation_depth
  return g


def gfun_vcorr(mo,FCl,tCl,FGa,Fox,po,n,kc,kt,kRCl,K,T,kRRH,tRRH):
  kRT = (1+K*(T-20))**(-1)
  FCl = FCl+tCl
  kRRH = kRRH+tRRH
  to = 0.0767
  tHydr = 1

  p = po*(tHydr*to**(-1))**n*kt*kc*kRT*kRRH*kRCl
  Vcorr = mo*p**(-1)*FCl*FGa*Fox*0.001
  g = Vcorr
  return g

def gfun_pt(Vcorr,theta,R,t):

  Vcorr = Vcorr+theta
  g = Vcorr*R*t

  return g

def gfun_apit(Vcorr,theta,R,do,t):

  nrv = len(R[0])
  Apit = R
  g = R
  Vcorr = Vcorr+theta
  Pt = Vcorr*R*t

  for i in range(nrv):
    pt = Pt[0][i]
    Do = do[0][i]

    if pt < Do:
      a = 2*pt*(1-(pt*Do**(-1))**2)**(0.5)
      Theta1 = 2*np.arcsin(a*Do**(-1))
      Theta2 = 2*np.arcsin(a*(2*pt)**(-1))
      A1 = 0.5*(Theta1*(Do*0.5)**2-a*np.absolute(Do*0.5-pt**2*Do**(-1)))
      A2 = 0.5*(Theta2*pt**2-a*pt**2*Do**(-1))

    if pt >= Do:
      Apit[0][i] = np.pi*4**(-1)*Do**2
    elif pt <= Do*2**(-0.5):
      Apit[0][i] = A1+A2
    else:
      Apit[0][i] = np.pi*4**(-1)*Do**2 - A1 + A2

  return Apit


def gfun_area_loss_pitting(Vcorr,theta,R,do,t):

  Apit = gfun_apit(Vcorr,theta,R,do,t)

  nrv = len(R[0])
  g = R

  for i in range(nrv):
    Do = do[0][i]
    Anom = np.pi*4**(-1)*Do**2
    if Anom < Apit[0][i]:
      g[0][i] = 1#Anom
    else:
      #g[0][i] = Anom-Apit[0][i]
      g[0][i] = Apit[0][i]*Anom**(-1)

  return g

def gfun_yield_loss_pitting(Vcorr,theta,R,do,t,ec):

  Qcorr = gfun_area_loss_pitting(Vcorr,theta,R,do,t)*100
  g = 1-(1-ec*Qcorr)

  return g

def gfun_area_loss_general(Vcorr,theta,R,do,t):

  nrv = len(R[0])
  g = R
  xcorr = Vcorr*t
  Anom = np.pi*4**(-1)*do**2
  Agen = np.pi*4**(-1)*(do-xcorr)**2
  g = 1-Agen*Anom**(-1)
  return g

def gfun_yield_loss_general(Vcorr,theta,R,do,t,ec):

  g = R*0

  return g

def gfun_resistance_pitting(Vcorr,theta,R,do,t,ec,ME,d,b,fc,fy):

  Apit = gfun_apit(Vcorr,theta,R,do,t)

  Anom = np.pi*4**(-1)*(do)**2

  Ast = Anom-Apit#R
  Qcorr = Apit*Anom**(-1)*100
  # for i in range(nrv):
  #   Do = do[0][i]
  #   Anom = np.pi*4**(-1)*Do**2
  #   aloch.append(Anom)
  #   # if Anom < Apit[0][i]:
  #   #   Ast[0][i] = 0
  #   # else:
  #   Ast[0][i] = Anom-Apit[0][i]
  #   Qcorr[0][i] = Apit[0][i]*Anom**(-1)*100

  # print 'Qcorr',np.mean(Qcorr)
  # print 'Ast2',np.mean(Ast)
  Ast = Ast*0.000001
  fyt = fy*(1-ec*Qcorr)
  do = do*0.001

  Anom = np.pi*4**(-1)*(do)**2

  Mnom = ME * Anom * fy * (d-((Anom*fy)*(1.7*fc*b)**(-1)))
  Mu = ME * Ast * fyt * (d-((Ast*fyt)*(1.7*fc*b)**(-1)))
  g = Mu*Mnom**(-1)

  # print 'Mu',np.mean(Mu)
  # print 'Mnom',np.mean(Mnom)

  # print 'mean Mu/Mn',np.mean(Mu*Mnom**(-1))
  # print 'stdv Mu/Mn',np.std(Mu*Mnom**(-1))
  # print 'CoV Mu/Mn',np.std(Mu*Mnom**(-1))*(np.mean(Mu*Mnom**(-1))**(-1))
  # print 'mean Mnom',np.mean(Mnom)
  # print 'stdv Mnom',np.std(Mnom)
  # print 'Cov Mnom',np.std(Mnom)*np.mean(Mnom)**(-1)
  return g


def gfun_resistance_general(Vcorr,theta,R,do,t,ec,ME,d,b,fc,fy):

  xcorr = Vcorr*t
  Ast = np.pi*4**(-1)*(do-xcorr)**2
  Ast = Ast*0.000001
  fyt = fy
  do = do*0.001

  Anom = np.pi*4**(-1)*(do)**2
  Mnom = ME * Anom * fy * (d-((Anom*fy)*(1.7*fc*b)**(-1)))
  Mu = ME * Ast * fyt * (d-((Ast*fyt)*(1.7*fc*b)**(-1)))

  # print 'Ast',np.mean(Ast)
  # print 'Anom',np.mean(Anom)

  # print 'mean Mnom',np.mean(Mnom)
  # print 'stdv Mnom',np.std(Mnom)
  # print 'Cov Mnom',np.std(Mnom)*np.mean(Mnom)**(-1)
  # print 'Mu',np.mean(Mu)
  # print 'Mnom',np.mean(Mnom)
  # print 'mean Mu/Mn',np.mean(Mu*Mnom**(-1))
  # print 'stdv Mu/Mn',np.std(Mu*Mnom**(-1))
  # print 'CoV Mu/Mn',np.std(Mu*Mnom**(-1))*(np.mean(Mu*Mnom**(-1))**(-1))
  g = Mu*Mnom**(-1)

  return g


def gfun_failure_pitting(Vcorr,theta,R,do,t,ec,ME,d,b,fc,fy,z,a,Re,G,Q):

  factor = gfun_resistance_pitting(Vcorr,theta,R,do,t,ec,ME,d,b,fc,fy)
  #factor = 1
  g = z*ME*Re*factor-a*G-(1-a)*Q

  return g


def gfun_failure_general(Vcorr,theta,R,do,t,ec,ME,d,b,fc,fy,z,a,Re,G,Q):

  factor = gfun_resistance_general(Vcorr,theta,R,do,t,ec,ME,d,b,fc,fy)
  #factor = 1
  g = z*ME*Re*factor-a*G-(1-a)*Q

  return g


def gfun_failure_nom(ME,z,a,Re,G,Q):

  g = z*ME*Re-a*G-(1-a)*Q

  return g
