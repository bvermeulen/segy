from pathlib import Path
import segyio

filename = Path('./data_files/himin.sgy')
filename = Path('./data_files/vibe_sweep/output.sgy')
filename = Path('./data_files/vibe_sweep/Haniya-GF-SGY/210426_03.sgy')
filename = Path('./data_files/vibe_sweep/Lekhwair-GF-SGY/local_200225_03.sgy')
with segyio.open(filename, ignore_geometry=True, endian='msb') as segy_obj:

    # Memory map file for faster reading (especially if file is big...)
    segy_obj.mmap()

    # Print binary header info
    print(segy_obj.bin)
    print(segy_obj.bin[segyio.BinField.Traces])
    print(segy_obj.bin[segyio.BinField.Interval])

    # Read headerword inline for trace 10
    print(segy_obj.header[1][segyio.TraceField.INLINE_3D])




    # Print inline and crossline axis
    print(segy_obj.xlines)
    print(segy_obj.ilines)