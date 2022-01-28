#!/bin/csh

module load nco
module load cdo
module load ferret

set echo on

cd /home/netapp-clima-users1/rnavarro/ANALYSIS/BLAKER/TEMP-tendency

set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS)

set i = 1

while ($i <= 4)
set EXP  = $RUN[$i]

ferret <<!

set region/z=0:5500/y=90S:90N/
set mem/size=9999

SET MEMORY/SIZE=888

use "/home/clima-archive2/rfarneti/RENE/DATA/MLD_BSO_$EXP.nc" !1
use "/home/clima-archive2/rfarneti/RENE/DATA/BSO_GLB_$EXP.nc" !2
use temp_diag_tend-$EXP.nc !3
use "/home/clima-archive2/rfarneti/RENE/DATA/area_t_$EXP.nc" !4

let mld_glb  = mld[j=1:200,d=1]
let bso_glb  = field[j=1:200,d=2]

let temptend_glb          = temp_tendency[d=3]*area_t[d=4]
let advection_glb         = temp_advection[d=3]*area_t[d=4]
let submeso_glb           = temp_submeso[d=3]*area_t[d=4]
let vdiffuse_diff_cbt_glb = temp_vdiffuse_diff_cbt[d=3]*area_t[d=4]
let neutral_diffusion_glb = neutral_diffusion_temp[d=3]*area_t[d=4]
let neutral_gm_glb        = neutral_gm_temp[d=3]*area_t[d=4]
let swh_glb               = sw_heat[d=3]*area_t[d=4]
let sfc_swflx_glb         = swflx[d=3]*area_t[d=4]

let temptend              = temptend_glb[i=@sum,j=1:200,k=1:50]
let advection             = advection_glb[i=@sum,j=1:200,k=1:50]
let submeso               = submeso_glb[i=@sum,j=1:200,k=1:50]
let vdiffuse_diff_cbt     = vdiffuse_diff_cbt_glb[i=@sum,j=1:200,k=1:50]
let neutral_diffusion     = neutral_diffusion_glb[i=@sum,j=1:200,k=1:50]
let neutral_gm            = neutral_gm_glb[i=@sum,j=1:200,k=1:50]
let swh                   = swh_glb[i=@sum,j=1:200,k=1:50]
let sfc_swflx             = sfc_swflx_glb[i=@sum,j=1:200]

let mask_mld = if(z[gz=temptend] LT mld_glb) then 1 else 0
let mask_bso = if(z[gz=temptend] LT bso_glb) then 1 else 0
let mask_tot = if(z[gz=temptend] LT mld_glb) then 0 else 1

set variable/bad = 0. mask_mld
set variable/bad = 0. mask_bso
set variable/bad = 0. mask_tot

let temptend_mld          = temptend[j=1:200,k=1:50]*mask_mld[j=1:200,k=1:50]
let advection_mld         = advection[j=1:200,k=1:50]*mask_mld[j=1:200,k=1:50]
let submeso_mld           = submeso[j=1:200,k=1:50]*mask_mld[j=1:200,k=1:50]
let vdiffuse_diff_cbt_mld = vdiffuse_diff_cbt[j=1:200,k=1:50]*mask_mld[j=1:200,k=1:50]
let neutral_diffusion_mld = neutral_diffusion[j=1:200,k=1:50]*mask_mld[j=1:200,k=1:50]
let neutral_gm_mld        = neutral_gm[j=1:200,k=1:50]*mask_mld[j=1:200,k=1:50]
let swh_mld               = swh[j=1:200,k=1:50]*mask_mld[j=1:200,k=1:50]

let temptend_bso          = temptend[j=1:200,k=1:50]*mask_bso[j=1:200,k=1:50,i=1]
let advection_bso         = advection[j=1:200,k=1:50]*mask_bso[j=1:200,k=1:50,i=1]
let submeso_bso           = submeso[j=1:200,k=1:50]*mask_bso[j=1:200,k=1:50,i=1]
let vdiffuse_diff_cbt_bso = vdiffuse_diff_cbt[j=1:200,k=1:50]*mask_bso[j=1:200,k=1:50,i=1]
let neutral_diffusion_bso = neutral_diffusion[j=1:200,k=1:50]*mask_bso[j=1:200,k=1:50,i=1]
let neutral_gm_bso        = neutral_gm[j=1:200,k=1:50]*mask_bso[j=1:200,k=1:50,i=1]
let swh_bso               = swh[j=1:200,k=1:50]*mask_bso[j=1:200,k=1:50,i=1]

let temptend_no_mld          = temptend[j=1:200,k=1:50]*mask_tot[j=1:200,k=1:50,i=1]
let advection_no_mld         = advection[j=1:200,k=1:50]*mask_tot[j=1:200,k=1:50,i=1]
let submeso_no_mld           = submeso[j=1:200,k=1:50]*mask_tot[j=1:200,k=1:50,i=1]
let vdiffuse_diff_cbt_no_mld = vdiffuse_diff_cbt[j=1:200,k=1:50]*mask_tot[j=1:200,k=1:50,i=1]
let neutral_diffusion_no_mld = neutral_diffusion[j=1:200,k=1:50]*mask_tot[j=1:200,k=1:50,i=1]
let neutral_gm_no_mld        = neutral_gm[j=1:200,k=1:50]*mask_tot[j=1:200,k=1:50,i=1]
let swh_no_mld               = swh[j=1:200,k=1:50]*mask_tot[j=1:200,k=1:50,i=1]

!!--temp tendencies for the STC and interior ocean heat budget (Mixed layer excluded)
let temptend_stc          = temptend_bso[y=-30:24@sum,k=@sum]          - temptend_mld[y=-30:24@sum,k=@sum]
let advection_stc         = advection_bso[y=-30:24@sum,k=@sum]         - advection_mld[y=-30:24@sum,k=@sum]
let submeso_stc           = submeso_bso[y=-30:24@sum,k=@sum]           - submeso_mld[y=-30:24@sum,k=@sum]
let vdiffuse_diff_cbt_stc = vdiffuse_diff_cbt_bso[y=-30:24@sum,k=@sum] - vdiffuse_diff_cbt_mld[y=-30:24@sum,k=@sum]
let neutral_diffusion_stc = neutral_diffusion_bso[y=-30:24@sum,k=@sum] - neutral_diffusion_mld[y=-30:24@sum,k=@sum]
let neutral_gm_stc        = neutral_gm_bso[y=-30:24@sum,k=@sum]        - neutral_gm_mld[y=-30:24@sum,k=@sum]
let swh_stc               = swh_bso[y=-30:24@sum,k=@sum]               - swh_mld[y=-30:24@sum,k=@sum]

let temptend_int          = temptend[y=-30:24@sum,k=@sum]              - temptend_bso[y=-30:24@sum,k=@sum]
let advection_int         = advection[y=-30:24@sum,k=@sum]             - advection_bso[y=-30:24@sum,k=@sum]
let submeso_int           = submeso[y=-30:24@sum,k=@sum]               - submeso_bso[y=-30:24@sum,k=@sum]
let vdiffuse_diff_cbt_int = vdiffuse_diff_cbt[y=-30:24@sum,k=@sum]     - vdiffuse_diff_cbt_bso[y=-30:24@sum,k=@sum]
let neutral_diffusion_int = neutral_diffusion[y=-30:24@sum,k=@sum]     - neutral_diffusion_bso[y=-30:24@sum,k=@sum]
let neutral_gm_int        = neutral_gm[y=-30:24@sum,k=@sum]            - neutral_gm_bso[y=-30:24@sum,k=@sum]
let swh_int               = swh[y=-30:24@sum,k=@sum]                   - swh_bso[y=-30:24@sum,k=@sum]

let temptend_tot          = temptend[y=-30:24@sum,k=@sum]              - temptend_mld[y=-30:24@sum,k=@sum]
let advection_tot         = advection[y=-30:24@sum,k=@sum]             - advection_mld[y=-30:24@sum,k=@sum]
let submeso_tot           = submeso[y=-30:24@sum,k=@sum]               - submeso_mld[y=-30:24@sum,k=@sum]
let vdiffuse_diff_cbt_tot = vdiffuse_diff_cbt[y=-30:24@sum,k=@sum]     - vdiffuse_diff_cbt_mld[y=-30:24@sum,k=@sum]
let neutral_diffusion_tot = neutral_diffusion[y=-30:24@sum,k=@sum]     - neutral_diffusion_mld[y=-30:24@sum,k=@sum]
let neutral_gm_tot        = neutral_gm[y=-30:24@sum,k=@sum]            - neutral_gm_mld[y=-30:24@sum,k=@sum] 
let swh_tot               = swh[y=-30:24@sum,k=@sum]                   - swh_mld[y=-30:24@sum,k=@sum]
let sfc_swflx_tot         = sfc_swflx[y=-30:24@sum] 

save/file=STC_temptend_${EXP}_GLB.nc/clobber temptend_tot
save/file=STC_temptend_${EXP}_GLB.nc/append  advection_tot
save/file=STC_temptend_${EXP}_GLB.nc/append  submeso_tot
save/file=STC_temptend_${EXP}_GLB.nc/append  vdiffuse_diff_cbt_tot
save/file=STC_temptend_${EXP}_GLB.nc/append  neutral_diffusion_tot
save/file=STC_temptend_${EXP}_GLB.nc/append  neutral_gm_tot
save/file=STC_temptend_${EXP}_GLB.nc/append  swh_tot

save/file=STC_temptend_${EXP}_GLB.nc/append  temptend_stc
save/file=STC_temptend_${EXP}_GLB.nc/append  advection_stc
save/file=STC_temptend_${EXP}_GLB.nc/append  submeso_stc
save/file=STC_temptend_${EXP}_GLB.nc/append  vdiffuse_diff_cbt_stc
save/file=STC_temptend_${EXP}_GLB.nc/append  neutral_diffusion_stc
save/file=STC_temptend_${EXP}_GLB.nc/append  neutral_gm_stc
save/file=STC_temptend_${EXP}_GLB.nc/append  swh_stc

save/file=STC_temptend_${EXP}_GLB.nc/append  temptend_int
save/file=STC_temptend_${EXP}_GLB.nc/append  advection_int
save/file=STC_temptend_${EXP}_GLB.nc/append  submeso_int
save/file=STC_temptend_${EXP}_GLB.nc/append  vdiffuse_diff_cbt_int
save/file=STC_temptend_${EXP}_GLB.nc/append  neutral_diffusion_int
save/file=STC_temptend_${EXP}_GLB.nc/append  neutral_gm_int
save/file=STC_temptend_${EXP}_GLB.nc/append  swh_int

!!--meridional sections heatbudget
save/file=STC_temptend_${EXP}_GLB_zonal.nc/clobber temptend_no_mld[y=-80:80,k=1:50]
save/file=STC_temptend_${EXP}_GLB_zonal.nc/append  advection_no_mld[y=-80:80,k=1:50]
save/file=STC_temptend_${EXP}_GLB_zonal.nc/append  submeso_no_mld[y=-80:80,k=1:50]
save/file=STC_temptend_${EXP}_GLB_zonal.nc/append  vdiffuse_diff_cbt_no_mld[y=-80:80,k=1:50]
save/file=STC_temptend_${EXP}_GLB_zonal.nc/append  neutral_diffusion_no_mld[y=-80:80,k=1:50]
save/file=STC_temptend_${EXP}_GLB_zonal.nc/append  neutral_gm_no_mld[y=-80:80,k=1:50]
save/file=STC_temptend_${EXP}_GLB_zonal.nc/append  swh_no_mld[y=-80:80,k=1:50]

exit
!
/bin/rm -f ferret.jnl*
@ i = $i + 1

end
