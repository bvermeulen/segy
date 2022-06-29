# read segy
from pathlib import Path
from re import L
import numpy as np
import matplotlib.pyplot as plt
import segyio

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

def plot_gf(ax, segy_filename, pilot_trace, gf_trace, endian='big', color='black'):
    with segyio.open(segy_filename, ignore_geometry=True, endian=endian,) as segy_obj:
        for trace_number in range(4):
            time_ms = []
            sample_val = []
            for i, val in enumerate(segy_obj.trace[trace_number]):
                time_ms.append(i * int(1000 * dt))
                sample_val.append(float(val))

            ax[trace_number].plot(time_ms, sample_val, color=color)

            if trace_number == pilot_trace:
                pilot = list(zip(time_ms, sample_val))

            if trace_number == gf_trace:
                gf = list(zip(time_ms, sample_val))

    return pilot, gf


def output_copy_trace(segy_filename_output, trace, ncopy):
    spec = segyio.spec()
    spec.iline = 0
    spec.xline = 0
    spec.samples = np.array(range(2250))
    spec.format = 5
    spec.tracecount = ncopy
    with segyio.create(segy_filename_output, spec) as segy_obj:
        bin_header = segy_obj.bin
        bin_header[segyio.BinField.Interval] = 4000
        bin_header[segyio.BinField.AuxTraces] = 0
        bin_header[segyio.BinField.SamplesOriginal] = 0
        bin_header[segyio.BinField.IntervalOriginal] = 0
        for i in range(ncopy):
            segy_obj.trace[i] = trace

ax1 = [None]*4
fig1, (ax1[0], ax1[1], ax1[2], ax1[3]) = plt.subplots(nrows=4, ncols=1, figsize=FIGSIZE)
pilot_1, gf_1 = plot_gf(ax1, segy_filename_haniya, 0, 3, endian='little', color='black')
fig1.suptitle('GF Haniya')
fig1.subplots_adjust(hspace=0.4)
ax1[0].set_title('pilot')
ax1[1].set_title('mass')
ax1[2].set_title('baseplate')
ax1[3].set_title('GF')

output_copy_trace(segy_filename_output, np.array(list(map(lambda x: x[1], gf_1)), np.float32), 500)

plt.tight_layout()
plt.show()
