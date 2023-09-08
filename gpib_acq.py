import pyvisa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time

N = 100  # Number of samples to acquire
GPIB_ADDRESS = 'GPIB0::22::INSTR'

rm = pyvisa.ResourceManager()
dmm = rm.open_resource(GPIB_ADDRESS)
dmm.read_termination = '\n'
dmm.write_termination = '\n'
dmm.write('CONF:FRES MIN,DEF')

data = []

input(f"Set all decades to zero. Press Enter to continue...")
print(f"\nNull measurement in progress\n")
for i in range(N):
    data.append(["All", 0, dmm.query('READ?')])
    
for decade in [0.01,0.1,1,10,100,1000,10000,100000]:
    if (decade >= 100): dmm.write(f'CONF:FRES {decade*10},DEF')
    for value in range(1,11):
        input(f"Set decade x{decade} to position {value} (Rest all zeros). Press Enter to continue...")
        print(f"\nmeasurements in progress for decade x{decade}, position {value}\n")
        for i in range(N):
            data.append([decade, value*decade, dmm.query('READ?')])

df = pd.DataFrame(data, columns=['decade', 'nominal', 'measured'])  
df.measured = df.measured.astype(float)
df.to_csv("readings.csv", index=None)
