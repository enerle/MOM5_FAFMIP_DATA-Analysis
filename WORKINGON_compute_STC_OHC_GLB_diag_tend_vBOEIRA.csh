#!/bin/csh
module load nco
module load cdo
module load ferret

set echo on

cd TEMP-tendency

set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS)

set i = 1

while ($i <= 4)
set EXP  = $RUN[$i]

ferret <<!

set region/z=0:5500/y=90S:90N/
set mem/size=9999

SET MEMORY/SIZE=888

use "/home/clima-archive2/rfarneti/RENE/DATA/MLD_BSO_$EXP.nc"  !1
use "/home/clima-archive2/rfarneti/RENE/DATA/BSO_GLB_$EXP.nc"  !2
use temp_diag_tend-$EXP.nc !3
use "/home/clima-archive2/rfarneti/RENE/DATA/area_t_$EXP.nc"   !4
use "/home/clima-archive2/rfarneti/RENE/DATA/dht_flux-only.nc" !5

let dx = geolon_t[d=4]
let dz = dht[d=5]

let mld_glb  = mld[j=1:200,d=1]
let bso_glb  = field[j=1:200,d=2]

let temptend_dz          = temp_tendency[d=3]/dz
let advection_dz         = temp_advection[d=3]/dz
let submeso_dz           = temp_submeso[d=3]/dz
let vdiffuse_diff_cbt_dz = temp_vdiffuse_diff_cbt[d=3]/dz
let neutral_diffusion_dz = neutral_diffusion_temp[d=3]/dz
let neutral_gm_dz        = neutral_gm_temp[d=3]/dz
let swh_dz               = sw_heat[d=3]/dz
let sfc_swflx_dz         = swflx[d=3]/dz

let temptend_glb          = temptend_dz*dx
let advection_glb         = advection_dz*dx
let submeso_glb           = submeso_dz*dx
let vdiffuse_diff_cbt_glb = vdiffuse_diff_cbt_dz*dx
let neutral_diffusion_glb = neutral_diffusion_dz*dx
let neutral_gm_glb        = neutral_gm_dz*dx
let swh_glb               = swh_dz*dx 
let sfc_swflx_glb         = sfc_swflx_dz*dx

let temptend              = temptend_glb[i=@sum,j=1:200,k=1:50]
let advection             = advection_glb[i=@sum,j=1:200,k=1:50]
let submeso               = submeso_glb[i=@sum,j=1:200,k=1:50]
let vdiffuse_diff_cbt     = vdiffuse_diff_cbt_glb[i=@sum,j=1:200,k=1:50]
let neutral_diffusion     = neutral_diffusion_glb[i=@sum,j=1:200,k=1:50]
let neutral_gm            = neutral_gm_glb[i=@sum,j=1:200,k=1:50]
let swh                   = swh_glb[i=@sum,j=1:200,k=1:50]
let sfc_swflx             = sfc_swflx_glb[i=@sum,j=1:200]

let mask_tot = if(z[gz=temptend] LT mld_glb) then 0 else 1

set variable/bad = 0. mask_tot

let temptend_no_mld          = temptend[j=1:200,k=1:50]*mask_tot[j=1:200,k=1:50,i=1]
let advection_no_mld         = advection[j=1:200,k=1:50]*mask_tot[j=1:200,k=1:50,i=1]
let submeso_no_mld           = submeso[j=1:200,k=1:50]*mask_tot[j=1:200,k=1:50,i=1]
let vdiffuse_diff_cbt_no_mld = vdiffuse_diff_cbt[j=1:200,k=1:50]*mask_tot[j=1:200,k=1:50,i=1]
let neutral_diffusion_no_mld = neutral_diffusion[j=1:200,k=1:50]*mask_tot[j=1:200,k=1:50,i=1]
let neutral_gm_no_mld        = neutral_gm[j=1:200,k=1:50]*mask_tot[j=1:200,k=1:50,i=1]
let swh_no_mld               = swh[j=1:200,k=1:50]*mask_tot[j=1:200,k=1:50,i=1]

!!--meridional sections heatbudget
!! expressed as longitudinal expressed sum (multiply by dx), instead of vertical-intergated sum (or divided by dz) 
save/file=STC_temptend_${EXP}_GLB_zonal_vBoeira.nc/clobber temptend_no_mld[y=-30:30,k=1:50]
save/file=STC_temptend_${EXP}_GLB_zonal_vBoeira.nc/append  advection_no_mld[y=-30:30,k=1:50]
save/file=STC_temptend_${EXP}_GLB_zonal_vBoeira.nc/append  submeso_no_mld[y=-30:30,k=1:50]
save/file=STC_temptend_${EXP}_GLB_zonal_vBoeira.nc/append  vdiffuse_diff_cbt_no_mld[y=-30:30,k=1:50]
save/file=STC_temptend_${EXP}_GLB_zonal_vBoeira.nc/append  neutral_diffusion_no_mld[y=-30:30,k=1:50]
save/file=STC_temptend_${EXP}_GLB_zonal_vBoeira.nc/append  neutral_gm_no_mld[y=-30:30,k=1:50]
save/file=STC_temptend_${EXP}_GLB_zonal_vBoeira.nc/append  swh_no_mld[y=-30:30,k=1:50]
exit
!

/bin/rm -f ferret.jnl*
@ i = $i + 1

end
