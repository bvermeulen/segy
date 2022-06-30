''' methods linking to the segyio module for:
      read_segy_file
      write_segy_file
      inspect
'''
from pathlib import Path
import numpy as np
import segyio
from pprint import pprint


class Segy:

    def __init__(self):
        pass

    def __repr__(self):
        return f'{help(self)}'

    @staticmethod
    def read_segy_file(filename: Path, endian: str = 'big') -> np.ndarray:
        ''' method to read segy file ignoring geometry information. It will give the trace
            data as a 2D numpy ndarray of size (m,n) [m traces, n samples]
                np.array([[S11..S1n], [S21..S2n] ...[Sm1..Smn]])
        '''
        with segyio.open(filename, ignore_geometry=True, endian=endian) as segy_obj:
            traces = segyio.tools.collect(segy_obj.trace[:])

        return traces

    @staticmethod
    def write_segy_file(
        filename: Path, traces: np.ndarray, dt: float,
        segy_format: int = 5, ncopy: int=1
    ) -> None:
        ''' method to write segy file.
            parameters:
              filename: Path, output filename
              traces: 2D numpy ndarray, data traces of size (m,n) [m traces, n samples]
              dt: float, sampling in millisecond
              segy_format: integer, segy output format (default: 5, IEEE float)
              ncopy: integer, number of times traces are repeated in output file (default: 1)
         '''
        if traces.shape[0] == 0:
            return

        spec = segyio.spec()
        spec.iline = 0
        spec.xline = 0
        spec.samples = np.array(range(traces.shape[1])) * dt * 1000
        spec.format = segy_format
        spec.tracecount = traces.shape[0] * ncopy
        with segyio.create(filename, spec) as segy_obj:
            bin_header = segy_obj.bin
            bin_header[segyio.BinField.Interval] = dt * 1000
            bin_header[segyio.BinField.AuxTraces] = 0
            bin_header[segyio.BinField.SamplesOriginal] = 0
            bin_header[segyio.BinField.IntervalOriginal] = 0
            for i, trace in enumerate(traces):
                for j in range(ncopy):
                    segy_obj.trace[i*ncopy + j] = np.array(trace, np.float32)

    @staticmethod
    def inspect(filename: Path, endian: str='big') -> None:
        ''' method to inspect segy filename
        '''
        with segyio.open(filename, ignore_geometry=True, endian=endian) as segy_obj:
            print('segy object meta data:')
            pprint(segy_obj.__dict__)
            print()

            print('binary header info:')
            pprint(dict(segy_obj.bin))
            print()
            print('trace header info first trace:')
            pprint(dict(segy_obj.bin.trace(0, segy_obj)))
            print()

            print('view of samples of first trace:')
            pprint(segy_obj.trace[0].view())
            print()

            # get basic attributes
            n_traces = segy_obj.tracecount
            sample_rate = segyio.tools.dt(segy_obj) / 1000
            n_samples = segy_obj.samples.size
            twt = segy_obj.samples

            print('general info:')
            print(
                f'Traces: {n_traces}, Samples: {n_samples}, '
                f'Sample rate: {sample_rate}ms, Trace length: {max(twt)}ms'
            )


def main():
    segy = Segy()
    f_in = Path('./data_files/vibe_sweep/Haniya-GF-SGY/210426_04.sgy')
    f_out = Path('./data_files/vibe_sweep/output_test.sgy')
    traces = segy.read_segy_file(f_in, endian='little')
    segy.write_segy_file(f_out, traces, 4, segy_format=5, ncopy=20)
    segy.inspect(f_out)


if __name__ == '__main__':
    main()
