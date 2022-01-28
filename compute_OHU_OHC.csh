#!/bin/csh

#module purge
module load nco
module load cdo
module load ferret

set echo on

cd DATA

set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS FAFALL FAFHEAT_FAFSTRESS)
set i = 1

while ($i <= 6)
set EXP  = $RUN[$i]

ferret <<!
!!------------------------------------------------------------------
!!---Ocean heat uptake OHC
!!------------------------------------------------------------------

use temp_$EXP.nc !1
use dht_$EXP.nc  !2
use area_t_$EXP.nc !3

let rho0   = 1035.0
let Cp     = 3989.0
let volume = area_t[d=3]*dht[l=61:70@ave,d=2]

SET MEMORY/SIZE=888

let heat_dht     = temp[l=61:70@ave,d=1]*dht[l=61:70@ave,d=2]
let OHU          = rho0*Cp*heat_dht[k=@sum]

let heat_volume  = temp[l=61:70@ave,d=1]*volume
let heat_content = rho0*Cp*heat_volume[i=@sum,k=@sum]

save/file=OHU_$EXP.nc/clobber OHU
save/file=heat_content_$EXP.nc/clobber heat_content

exit
!

/bin/rm -f ferret.jnl*
@ i = $i + 1
end
