#!/usr/bin/env python3

from Falcom import ED9
from Falcom.Common import *
import pathlib

def main(filename):
    t_name = ED9.DataTable(fs = fileio.FileStream(filename, encoding = GlobalConfig.DefaultEncoding, endian = GlobalConfig.StructEndian))
    path = pathlib.Path(filename)
    open(f'{path.parent / path.stem}.py', 'wb').write('\n'.join(t_name.toPython(path.name)).encode('UTF8'))
    # console.pause('done')

if __name__ == '__main__':
    for i in sys.argv[1:]:
        Try(main, i)
