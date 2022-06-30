import sys
from pathlib import Path
from segy_interface import Segy


def main(filename, endian='little'):
    segy = Segy()
    segy.inspect(filename, endian)


if __name__ == '__main__':
    filename = Path('./data_files/himin.sgy')
    filename = Path('./data_files/vibe_sweep/output.sgy')
    filename = Path('./data_files/vibe_sweep/Haniya-GF-SGY/210426_03.sgy')
    filename = Path('./data_files/vibe_sweep/Test_1_prodsweep_75_0515.sgy')
    filename = Path('./data_files/vibe_sweep/output.sgy')
    filename = Path('./data_files/vibe_sweep/Lekhwair-GF-SGY/local_200225_03.sgy')
    endian = 'big'

    args = sys.argv
    if len(args) > 2:
        filename = Path(args[1])
        endian = args[2]

    elif len(args) > 1:
        filename = Path(args[1])

    print(f'inspect: {filename} (endian: {endian})')
    print()
    main(filename, endian=endian)
