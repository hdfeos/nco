#!/bin/sh

# $Header: /data/zender/nco_20150216/nco/data/nco_bnch.sh,v 1.2 2004-07-20 00:18:24 zender Exp $

# Purpose: Benchmark NCO performance

# Usage:

# Create file with dimension sizes
ncgen -b -o ${DATA}/mie/big.nc ~/nco/data/big.cdl

# Create file with decadal differences in dimension sizes
ncap -D 3 -O \
-s "wvl_1e0[wvl_1e0]=1.0f" \
-s "wvl_1e1[wvl_1e1]=1.0f" \
-s "wvl_1e2[wvl_1e2]=1.0f" \
-s "wvl_1e3[wvl_1e3]=1.0f" \
-s "wvl_1e4[wvl_1e4]=1.0f" \
-s "wvl_1e5[wvl_1e5]=1.0f" \
-s "wvl_1e6[wvl_1e6]=1.0f" \
-s "wvl_1e7[wvl_1e7]=1.0f" \
-s "wvl_1e8[wvl_1e8]=1.0f" \
${DATA}/mie/big.nc ${DATA}/mie/big.nc

# Benchmark arithmetic operations on large files
timex ncwa -O -a wvl_1e8 -v wvl_1e8 ${DATA}/mie/big.nc ${DATA}/mie/foo.nc;ncks -H ${DATA}/mie/foo.nc
date;ncwa -O ${DATA}/mie/big.nc ${DATA}/mie/foo.nc;date;ncks -H ${DATA}/mie/foo.nc
date;ncwa -O -a wvl_1e8 -v wvl_1e8 ${DATA}/mie/big.nc ${DATA}/mie/foo.nc;date;ncks -H ${DATA}/mie/foo.nc

# Results: 
# elnino gcc 3.3.4 with restrict keyword     20040719: 11m31s
# elnino gcc 3.3.4 without restrict keyword  20040719: 10m20s
# esmf04m xlc 6.x with restrict keyword      20040719: 22s
# esmf04m xlc 6.x without restrict keyword   20040719: 25s
# 2^32=4294967296
# 2^31=2147483648
# 10^9=1000000000
# 10^8= 100000000

