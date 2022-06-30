# read segy
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from segy_interface import Segy

segy_filename_haniya = Path('./data_files/vibe_sweep/Haniya-GF-SGY/210426_03.sgy')
segy_filename_output = Path('./data_files/vibe_sweep/output.sgy')
dt = 4 / 1000 # sampling interval is 4 ms
df = 1 / dt # sampling frequency
lowcut = 0.5
highcut = 100.0
pi = np.pi
sweep_length = 9000 # ms
max_lag = 129
FIGSIZE = (12, 8)
segy = Segy()

def plot_gf(ax, segy_filename, pilot_trace, gf_trace, endian='big', color='black'):
    traces = segy.read_segy_file(segy_filename, endian=endian)
    for trace_number, trace in enumerate(traces):
        time_ms = []
        sample_val = []
        for i, val in enumerate(trace):
            time_ms.append(i * int(1000 * dt))
            sample_val.append(float(val))

        ax[trace_number].plot(time_ms, sample_val, color=color)

        if trace_number == pilot_trace:
            pilot = list(zip(time_ms, sample_val))

        if trace_number == gf_trace:
            gf = list(zip(time_ms, sample_val))

    return pilot, gf

ax1 = [None]*4
fig1, (ax1[0], ax1[1], ax1[2], ax1[3]) = plt.subplots(nrows=4, ncols=1, figsize=FIGSIZE)
pilot_1, gf_1 = plot_gf(ax1, segy_filename_haniya, 0, 3, endian='little', color='black')
fig1.suptitle('GF Haniya')
fig1.subplots_adjust(hspace=0.4)
ax1[0].set_title('pilot')
ax1[1].set_title('mass')
ax1[2].set_title('baseplate')
ax1[3].set_title('GF')

segy.write_segy_file(
    segy_filename_output,
    np.array([list(map(lambda x: x[1], gf_1))], np.float32),
    int(dt * 1000),
    segy_format=5,
    ncopy=1
)

plt.tight_layout()
plt.show()
