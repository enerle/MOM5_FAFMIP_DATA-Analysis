#!/bin/csh

#module purge
module load nco
module load cdo
module load ferret

set echo on

#cd DATA
cd /home/clima-archive2/rfarneti/RENE/DATA
#set RUN = (flux-only FAFSTRESS FAFWATER FAFHEAT FAFALL)
set RUN = (FAFALL flux-only)

set i = 1

while ($i <= 5)
set EXP  = $RUN[$i]

ferret <<!

use MLD_BSO_$EXP.nc !1
use BSO_GLB_$EXP.nc !2
use temp_$EXP.nc    !3
use area_t_$EXP.nc  !4
use dht_$EXP.nc     !5
use "/home/netapp-clima-users1/rnavarro/ANALYSIS/regionmask_v6.nc" !6

set region/y=90S:90N/z=0:5000
set mem/size=999

let rho    = 1035.0
let cp     = 3989.0
let volume = area_t[d=4]*dht[d=5]

let mld_glb  = mld[j=1:200,d=1]
let bso_glb  = field[j=1:200,d=2]

let temp_glb = temp[d=3]
let temp_vol = temp_glb*volume

let heat_vol = rho*cp*temp_vol[i=@sum]

let mask_mld = if(z[gz=temp_vol] LT mld_glb) then 1 else 0 !!why the last k-level disappear?
let mask_bso = if(z[gz=temp_vol] LT bso_glb) then 1 else 0
let mask_tot = if(z[gz=temp_vol] LT mld_glb) then 0 else 1

set variable/bad = 0. mask_mld
set variable/bad = 0. mask_bso
set variable/bad = 0. mask_tot

let heat_vol_tot    = heat_vol[j=1:200,k=1:50,l=1:70]
let heat_vol_mld    = heat_vol[j=1:200,k=1:50,l=1:70]*mask_mld[j=1:200,k=1:50]
let heat_vol_bso    = heat_vol[j=1:200,k=1:50,l=1:70]*mask_bso[j=1:200,k=1:50,i=1]
let heat_vol_no_mld = heat_vol[j=1:200,k=1:50,l=1:70]*mask_tot[j=1:200,k=1:50]

let ohc_mld = heat_vol_mld[y=-30:24@sum,k=@sum,l=1:70] 
let ohc_stc = heat_vol_bso[y=-30:24@sum,k=@sum,l=1:70] - heat_vol_mld[y=-30:24@sum,k=@sum,l=1:70]
let ohc_int = heat_vol_tot[y=-30:24@sum,k=@sum,l=1:70] - heat_vol_bso[y=-30:24@sum,k=@sum,l=1:70]
let ohc_tot = heat_vol_tot[y=-30:24@sum,k=@sum,l=1:70] - heat_vol_mld[y=-30:24@sum,k=@sum,l=1:70]

!!--meridional zonally and vertically integrated timemean heat content
let ohc_mld_zonal = heat_vol_mld[y=-30:24,k=@sum,l=1:70]
let ohc_stc_zonal = heat_vol_bso[y=-30:24,k=@sum,l=1:70] - heat_vol_mld[y=-30:24,k=@sum,l=1:70]
let ohc_int_zonal = heat_vol_tot[y=-30:24,k=@sum,l=1:70] - heat_vol_bso[y=-30:24,k=@sum,l=1:70]
let ohc_tot_zonal = heat_vol_tot[y=-30:24,k=@sum,l=1:70] - heat_vol_mld[y=-30:24,k=@sum,l=1:70]

save/file=STC_OHC_${EXP}_GLB_time_v2.nc/clobber ohc_mld
save/file=STC_OHC_${EXP}_GLB_time_v2.nc/append  ohc_tot
save/file=STC_OHC_${EXP}_GLB_time_v2.nc/append  ohc_stc
save/file=STC_OHC_${EXP}_GLB_time_v2.nc/append  ohc_int
save/file=STC_OHC_${EXP}_GLB_time_v2.nc/append  ohc_mld_zonal
save/file=STC_OHC_${EXP}_GLB_time_v2.nc/append  ohc_tot_zonal
save/file=STC_OHC_${EXP}_GLB_time_v2.nc/append  ohc_stc_zonal
save/file=STC_OHC_${EXP}_GLB_time_v2.nc/append  ohc_int_zonal

save/file=STC_OHC_${EXP}_GLB_zonal_v2.nc/clobber  heat_vol_no_mld[y=-80:80,k=1:50,l=1:70]

exit
!

/bin/rm -f ferret.jnl*
@ i = $i + 1
end
