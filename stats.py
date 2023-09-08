import pandas as pd
import numpy as np
df = pd.read_csv("readings.csv")
df_temp_stat = df.groupby(by=['decade','nominal']).agg(mean=('measured','mean'), stdev=('measured','std')).reset_index()
df_temp_stat['unc_low'] = df_temp_stat.apply(lambda x: x['mean']-2*x['stdev'], axis=1)
df_temp_stat['unc_high'] = df_temp_stat.apply(lambda x: x['mean']+2*x['stdev'], axis=1)
null_value = df_temp_stat[df_temp_stat.decade=='All']['mean'].values[0]
df_temp_stat['measured_zero_adj'] = df_temp_stat['mean'].apply(lambda x: x-null_value)
df_temp_stat['uncertainty_low'] = df_temp_stat['unc_low'].apply(lambda x: x-null_value)
df_temp_stat['uncertainty_high'] = df_temp_stat['unc_high'].apply(lambda x: x-null_value)
df_temp_stat['spec_low'] = df_temp_stat.nominal.apply(lambda x: x-x*0.03/100-0.0005)
df_temp_stat['spec_high'] = df_temp_stat.nominal.apply(lambda x: x+x*0.03/100+0.0005)
df_temp_stat[df_temp_stat.decade!='All'].to_csv("biddle_perf_test_automated.csv",index=None)
