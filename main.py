import numpy as np
import struct
import f90nml
import os
from shutil import copyfile

if __name__=="__main__":
    nz = 59
    ny = 100
    nx = 200
    filename = "seatmp_prs_lo0100xhi0200_2012060200_00000000_fcsterr"
    flds = filename.split("_")
    grds = flds[2].split("x")
    for g in grds:
        print(g[-4:])
    nx = int(grds[0][-4:])
    ny = int(grds[1][-4:])
    print("ny, nx = %i, %i" % (ny, nx))

    for k,fld in enumerate(flds):
        print ("%i: %s" % (k,fld))
    f = open(filename, "wb")
    mydata = np.random.random(nz * ny * nx)
    print(mydata)
    myfmt = 'f' * len(mydata)
    #  You can use 'd' for double and < or > to force endinness
    bin = struct.pack(myfmt, *mydata)
    print(bin)
    f.write(bin)
    f.close()
    xbash = np.fromfile(filename, dtype='f')
    print(xbash.shape)
    print(xbash)

    nml = {
        'config_nml': {
            'input': 'wind.nc',
            'steps': 864,
            'layout': [8, 16],
            # 'visc': 0.0001,
            'use_biharmonic': False
        }
    }
    print(nml)

    # if os.path.exists('namelist_org.nml'):
    #     copyfile('namelist_org.txt','namelist_new.nml')
    nml_new = f90nml.read('namelist_org.txt')
    nml_new['config_nml']['steps'] = 423
    print(nml_new)
    print(nml_new['config_nml']['visc'])
    nml_new['config_nml']['visc'] = 0.001
    if os.path.exists('namelist_new.nml'):
        os.remove('namelist_new.nml')
    nml_new.write('namelist_new.nml')
