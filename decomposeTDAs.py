# originally from https://github.com/superfan89/IDMSKconv
# reference: https://github.com/hoverruan/IDMSKconv/blob/master/decomposeTDAs.py
# python3

import zlib
import struct
import re
import os

typeIndex = {'ULONG': 4,
             'U24': 3,
             'USHORT': 2,
             'UBYTE': 1,
             'LINK': 0,
             'DATA': 0}


class decompose:
    def __init__(self, dir, outdir):
        self.dir = dir
        self.outdir = outdir
        self.formatStr = [0, 0, 0]
        self.packLongSize = struct.calcsize('L')
        self.parseFormat()
        self.writeOffsetIndex()

    def parseFormat(self):
        select = 0
        fconfig = open(os.path.join(self.dir, 'config.cft'), 'r')
        for line in fconfig:
            result = re.match(r'\$(\S+)\s*=\s*(\S+)', line)
            if result:
                if result.group(1) == 'CONTENT,OFFSET':
                    self.formatStr[1] = typeIndex[result.group(2)]
                    select = 2
                else:
                    self.formatStr[select] += typeIndex[result.group(2)]

    def writeOffsetIndex(self):
        self.offsets = []
        i = 0
        fdata = open(os.path.join(self.dir, 'files.dat'), 'rb')
        while True:
            i += 1
            if(len(fdata.read(self.formatStr[0])) == 0):
                break
            self.offsets.append(struct.unpack(
                'L', fdata.read(self.formatStr[1])+(self.packLongSize-self.formatStr[1])*b'\x00')[0])
            fdata.read(self.formatStr[2])

    def inflateTDA(self):
        fin = open(os.path.join(self.dir, 'CONTENT.tda'), 'rb')
        fdst = open(os.path.join(self.outdir, 'output'), 'wb')
        findex = open(os.path.join(self.dir, 'CONTENT.tda.tdz'), 'rb')
        byte = []
        while True:
            bin = findex.read(8)
            if len(bin) == 0:
                break
            byte.append(struct.unpack('ii', bin))
        i = 0
        print('Now decompressing...')
        for xi, bytei in byte:
            i += 1
            dedata = zlib.decompress(fin.read(bytei))
            fdst.write(dedata)
        print('Done!Total %d entries.' % i)

    def writeFiles(self):
        fin = open(os.path.join(self.dir, 'NAME.tda'), 'rb')
        raw = fin.read()
        name = raw.split(b'\x00')
        fin = open(os.path.join(self.outdir, 'output'), 'rb')
        for i in range(len(self.offsets)):
            storepath = os.path.join(self.outdir, name[i].decode("utf8"))
            if os.path.exists(storepath):
                for i_duplicate in range(1, 11):  # 万一有十个重复的呢
                    storepath = os.path.join(
                        self.outdir, f'{i_duplicate}dup_' + name[i].decode("utf8"))
                    if not os.path.exists(storepath):
                        print(f"Find duplicate files, stored in {storepath}")
                        break
            fout = open(storepath, 'wb')
            if(i == len(self.offsets)-1):
                fout.write(fin.read()[:-1])
            else:
                fout.write(fin.read(self.offsets[i+1]-self.offsets[i])[:-1])
            print(f'Now writing separate files: {i+1}\r', end='', flush=True)
        print('\nDone!')
