#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 16:39:28 2022

@author: jasmindersingh

ECU andf ICU SATURATED
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


def simulation(p, t):
   # inflow
   pin = 6  # patient/hr into ER

   # constants
   c1 = 0.8 #Covid patients into ICU
   c2 = 0.1 #Covid death rate out of ICU
   
   #ECU
   nurses = 1 #1 nurse = 4 patients
   ventilators = 5 # 1 ventilator = 1 patient
   ctscan = 8 # 1 CT-Scan = 5 patients
   
   #ECU capacity
   ecu_capacity = min(4*nurses, ventilators, 5*ctscan)
   
   #ICU
   doctors = 4 # 1 doctor = 8 patients
   respirators =2 # 2 respirator = 1 patient
   beds = 5 # 1 bed = 1 patient
   
   #ECU capacity
   icu_capacity = min(8*doctors, 0.5*respirators, beds)
   
   # outflow
   pout1 = c1 * p[0] * (nurses/4) * ventilators * (ctscan/5)  
   pout2 = c2 * p[1] * (doctors/8) * (2*respirators) * beds
   
   # differential equations
   dpdt1 = (pin   - pout1) / ecu_capacity
   dpdt2 = (pout1 - pout2) / icu_capacity
   
   # overflow conditions
   if p[0]>=10 and dpdt1>=0:
       dpdt1 = 0
   if p[1]>=10 and dpdt2>=0:
       dpdt2 = 0
   dpdt = [dpdt1,dpdt2]
   return dpdt

# integrate the equations
t = np.linspace(0,20) # times to report solution
p0 = [0,0]            # initial conditions for number of patients
y = odeint(simulation,p0,t) # integrate

# plot results
plt.figure(1)
plt.plot(t,y[:,0],'b-')
plt.plot(t,y[:,1],'r--')
plt.xlabel('Time (hrs)')
plt.ylabel('Patients (person)')
plt.legend(['ECU','ICU'])
plt.show()