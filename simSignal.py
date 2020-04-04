#!/usr/bin/python3

import numpy
import argparse 
import time
import math
import sys
from epics import caput, caget

def usage():
  print('usage' + sys.argv[0] + ' [options]')
  print('Writes a primitive signal form (ramp or sine) to a given EPICS PV')
  print('--type        "ramp" or "sine" functions available')
  print('--period      signal periodicity in seconds [float]')       
  print('--magnitude   signal magnitude [float]')
  print('--offset      (OPTIONAL, defaults to 0) signal offset [float]')
  print('--pv          PV name to write signal to')
  print('--expire      (OPTIONAL, defaults to 100 seconds) expiration time to stop writing signal to PV') 
  exit(1)

parser = argparse.ArgumentParser()
parser.add_argument('--signal')
parser.add_argument('--magnitude',type=float)
parser.add_argument('--period',type=float)
parser.add_argument('--offset', type=float)
parser.add_argument('--pv')
parser.add_argument('--expire', type=float)

args = parser.parse_args()
signal = args.signal
magnitude = args.magnitude
period = args.period
pv = args.pv

if args.offset is None:
  offset = 0
else:
  offset = args.offset

if args.expire is None:
  expire = 100
else:
  expire = args.expire

if signal != 'ramp' and signal != 'sine':
  usage()

if magnitude is None or period is None or pv is None:
  usage()

ellapsed = 0
timestep = 0
# Get current PV value to allow restoration on completion
oldValue = caget(pv)
while ellapsed < expire:
  time.sleep(0.1)
  if timestep > period:
    timestep = 0
  else:
    timestep += 0.1
  ellapsed += 0.1
  output_ramp = magnitude * ellapsed / period + offset
  output_sine = magnitude * math.sin ( 2 * math.pi * ellapsed / period) + offset
  if signal == 'ramp':
    caput(pv, output_ramp)
  elif signal == 'sine':
    caput(pv, output_sine)

#Reset PV to its original value
caput(pv, oldValue)
