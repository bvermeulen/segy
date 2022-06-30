from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from segy_interface import Segy

file_min_phase = Path('./data_files/himin.sgy')
file_zero_phase = Path('./data_files/hilin.sgy')

dt = 4       # sampling interval is 4 ms
df = 1 / dt  # sampling frequency
pi = np.pi
record_length = 4000  # ms
segy = Segy()

earth_model = [(500, +1.0), (1000, -0.5),
               (1200, +0.6), (2000, +0.2),
               (2100, -0.3), (2600, -0.4),
               (3100, +0.4),]
noise_factor = 0.05

fig, ax = plt.subplots(nrows=4, ncols=1, figsize=(8, 7))

traces = segy.read_segy_file(file_min_phase)
trace_samples = traces[3]
pilot_samples= [(i*dt, sample) for i, sample in enumerate(trace_samples)]
pilot_min_df = pd.DataFrame(pilot_samples, columns=['Time', 'Amplitude'])
pilot_min_trace = pilot_min_df['Amplitude']

traces = segy.read_segy_file(file_zero_phase)
trace_samples = traces[3]
pilot_samples= [(i*dt, sample) for i, sample in enumerate(trace_samples)]
pilot_zero_df = pd.DataFrame(pilot_samples, columns=['Time', 'Amplitude'])
pilot_zero_trace = pilot_zero_df['Amplitude']

earth_trace = [[i * dt, noise_factor * (0.5 - np.random.random_sample())]
               for i in range(int(record_length * df))]
for (t, val) in earth_model:
    earth_trace[int(t * df)][1] += val

earth_df = pd.DataFrame(earth_trace, columns=['Time', 'Amplitude'])

time = earth_df['Time']
earth_trace = earth_df['Amplitude']
ax[0].set_title('Earth')
ax[0].set_xlim(0, 17000)
ax[0].plot(time, earth_trace)

time = pilot_min_df['Time']
ax[1].set_title('Pilot')
ax[1].set_xlim(0, 17000)
ax[1].plot(time, pilot_min_trace)

convolved_trace = np.convolve(earth_trace, pilot_min_trace)
time = [(i * dt) for i in range(len(convolved_trace))]
ax[2].set_title('Convolved trace')
ax[2].set_xlim(0, 17000)
ax[2].plot(time, convolved_trace)

scaling = len(pilot_min_trace) * len(pilot_min_trace) * dt * dt * np.max(pilot_min_trace)
correlated_trace = np.correlate(convolved_trace, pilot_min_trace) / scaling
time = [(i * dt) for i in range(len(correlated_trace))]
ax[3].set_title('correlated')
ax[3].set_xlim(0, 17000)
ax[3].plot(time, correlated_trace)

correlated_trace = np.array([correlated_trace], np.float32)
segy.write_segy_file(
    Path('./data_files/vibe_sweep/output_correlated.sgy'),
    correlated_trace,
    dt,
    ncopy=100
)
plt.tight_layout()
plt.show()
