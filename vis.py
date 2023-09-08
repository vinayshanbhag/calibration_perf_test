import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

df = pd.read_csv("biddle_perf_test_automated.csv")
df['unc_top'] = df.apply(lambda x: ((x['uncertainty_high']-x['nominal'])/x['nominal'])*100, axis=1)
df['unc_bottom'] = df.apply(lambda x: ((x['uncertainty_low']-x['nominal'])/x['nominal'])*100, axis=1)
df['meas_dev'] = df.apply(lambda x: ((x['measured_zero_adj']-x['nominal'])/x['nominal'])*100, axis=1)
df['spec_top'] = df.apply(lambda x: ((x['spec_high']-x['nominal'])/x['nominal'])*100, axis=1)
df['spec_bottom'] = df.apply(lambda x: ((x['spec_low']-x['nominal'])/x['nominal'])*100, axis=1)
df['nominal_norm'] = df.apply(lambda x: 0, axis=1)
range_labels = {0:'0.01 ',10:'0.1 ',20:'1 ',30:'10 ',40:'100 ',50:'1 k',60:'10 k',70:'100 k'}
fig, ax = plt.subplots(nrows=4, ncols=2,figsize=(15, 25))
columns = 2
row = 0
for i in range(8):
  n,m = i*10, i*10+10
  col = i%columns
  #print(f"n={i*10}, m={i*10+10}, [{row}, {i%columns}]")

  ax[row,col].plot(df[n:m].nominal, df[n:m].nominal_norm,color='black', marker='x',linestyle='', label='Nominal Value')
  ax[row,col].plot(df[n:m].nominal, df[n:m].meas_dev,color='tab:blue', marker='s',linestyle='', label='Measured Value')
  ax[row,col].plot(df[n:m].nominal, df[n:m].spec_bottom, color='tab:red', marker='', linestyle='-',label='Specification Limits')
  ax[row,col].plot(df[n:m].nominal, df[n:m].spec_top, color='tab:red', marker='', linestyle='-', label='_nolegend_')
  ax[row,col].plot(df[n:m].nominal, df[n:m].unc_bottom, color='tab:blue', marker='_',linestyle='', label='_nolegend_')
  ax[row,col].plot(df[n:m].nominal, df[n:m].unc_top, color='tab:blue', marker='_',linestyle='', label='_nolegend_')
  ax[row,col].grid(True);
  ax[row,col].set_xticks(df[n:m].nominal);
  ax[row,col].set_xticklabels(['1','2','3','4','5','6','7','8','9','X']);
  ax[row,col].set_xlabel('Dial Position')
  ax[row,col].set_ylabel('Deviation from Nominal %')
  ax[row,col].fill_between(df[n:m].nominal,df[n:m].unc_bottom, df[n:m].unc_top,
                    color = 'lightblue', alpha=0.3, label='Measured ± Uncertainty')
  ax[row,col].set_title(f"x{range_labels[n]}Ω range");
  if (row==0 and col==1):ax[row,col].legend( loc="upper right")
  if (i%columns==1): row+=1

#plt.figlegend(lines, labels, loc = 'lower center', ncol=5, labelspacing=0.)

fig.suptitle(f"Calibration Resistance Standard\nPerformance Test Results\n");
fig.tight_layout();
plt.savefig('perftest.png')
