''' correlate and output to file
'''
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from segy_interface import Segy

segy = Segy()
gf_file = Path('./data_files/vibe_sweep/Haniya-GF-SGY/210426_01.sgy')
data_file = Path('./data_files/vibe_sweep/Test_1_prodsweep_75_0515.sgy')
output_file = Path('./data_files/vibe_sweep/Test_1_correlated.sgy')
dt = 4
FIGSIZE = (12, 8)

fig, ax = plt.subplots(nrows=4, ncols=1, figsize=FIGSIZE)


# get GF reference
traces = segy.read_segy_file(gf_file, endian='little')
trace_samples = traces[0]
pilot_samples= [(i*dt, sample) for i, sample in enumerate(trace_samples)]
pilot_df = pd.DataFrame(pilot_samples, columns=['Time', 'Amplitude'])
pilot_trace = np.array(pilot_df['Amplitude'], np.float32)

# get data trace
traces = segy.read_segy_file(data_file, endian='little')
trace_samples = traces[2]
data_samples = [(i*dt, sample) for i, sample in enumerate(trace_samples)]
data_df = pd.DataFrame(data_samples, columns=['Time', 'Amplitude'])
data_trace = np.array(data_df['Amplitude'], np.float32)

scaling = 1.0 # len(pilot_trace) * len(pilot_trace) * dt * dt * np.max(pilot_min_trace)
correlated_trace = np.correlate(data_trace, pilot_trace) / scaling

time = pilot_df['Time']
ax[0].set_title('Pilot')
ax[0].set_xlim(0, 17000)
ax[0].plot(time, pilot_trace)

time = data_df['Time']
ax[1].set_title('Data')
ax[1].set_xlim(145_000, 162_000)
ax[1].plot(time[32_500:53_500], data_trace[32_500:53_500])

time = [(i * dt) for i in range(len(correlated_trace))]
ax[2].set_title('correlated')
ax[2].set_xlim(0, 150_000)
ax[2].plot(time, correlated_trace)

traces = np.vstack((data_trace[:42000], correlated_trace[:42000]))
segy.write_segy_file(
    output_file, traces, dt
)
plt.show()
