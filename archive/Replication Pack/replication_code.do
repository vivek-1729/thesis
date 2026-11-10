
clear


*********************************
**# 1 Gravity Model
*********************************
clear

use gravity_trade_data.dta


**# 1.1 Variable construction
gen good_share = good_count/(good_tot1+good_tot2)
gen same_reg = (region1 == region2)
gen lat_diff = abs(lat1-lat2)

gen ldist_ptime_da = ln(p_sea_time_hr/24)

gen ldist_ptime_da_sq = (ldist_ptime_da)^2
gen ldist_ptime_da_rt = sqrt(ldist_ptime_da)

** FE for PPML
tabulate pcode1, generate(pcode1_dummy_)
tabulate pcode2, generate(pcode2_dummy_)
global city_fe pcode1_dummy_* pcode2_dummy_*

* exclude one dummy
drop pcode1_dummy_7 pcode2_dummy_7

tabulate region1, generate(region1_dummy_)
tabulate region2, generate(region2_dummy_)
global region_fe region1_dummy_* region2_dummy_*


**# 1.2 Descriptive Statistics 
sum pair_id

* percentage of pairs not roman
sum pair_id if (region1 != 100 & region2 != 100)

* percentage of pairs not peripheral
sum pair_id if (region1 != 100 & region1 != 250 & region1 <= 600 & region2 != 100 & region2 != 250 & region2 <= 600)


**# 1.3 Regressions 

** Base Model
ppmlhdfe good_count ldist_ptime_da same_reg lat_diff $city_fe


** Robustness 

* Product shares
ppmlhdfe good_share ldist_ptime_da same_reg lat_diff $city_fe

* Sequential drop of cities
ppmlhdfe good_count ldist_ptime_da same_reg lat_diff $city_fe if (pcode1 != 254 & pcode2 != 254)

ppmlhdfe good_count ldist_ptime_da same_reg lat_diff $city_fe if (pcode1 != 251 & pcode2 != 251)

ppmlhdfe good_count ldist_ptime_da same_reg lat_diff $city_fe if (pcode1 != 651 & pcode2 != 651)

ppmlhdfe good_count ldist_ptime_da same_reg lat_diff $city_fe if (pcode1 != 507 & pcode2 != 507)

ppmlhdfe good_count ldist_ptime_da same_reg lat_diff $city_fe if (pcode1 != 506 & pcode2 != 506)

ppmlhdfe good_count ldist_ptime_da same_reg lat_diff $city_fe if (pcode1 != 101 & pcode2 != 101)

ppmlhdfe good_count ldist_ptime_da same_reg lat_diff $city_fe if (pcode1 != 103 & pcode2 != 103)



*****************************************************************************
*****************************************************************************



************************************
**# 2 Nonlinear Analysis
************************************
clear

use gravity_trade_data_zeros.dta


**# 2.1 Variable construction

* Trade and distance variables
gen good_share = good_count/(good_tot1+good_tot2)
gen ldist_ptime_da = ln(p_sea_time_hr/24)
gen ldist_ptime_da_rt = sqrt(ldist_ptime_da)

* FE for PPML
tabulate pcode1, generate(pcode1_dummy_)
tabulate pcode2, generate(pcode2_dummy_)
global city_fe pcode1_dummy_* pcode2_dummy_*

tabulate region1, generate(region1_dummy_)
tabulate region2, generate(region2_dummy_)
global region_fe region1_dummy_* region2_dummy_*

* Other controls
gen same_region = (region1 == region2)
gen close_dist = (ldist_ptime_da < 2.65)
gen lat_diff = abs(lat1-lat2)


**# 2.2 Regressions

* Polynomial Model
ppmlhdfe good_count ldist_ptime_da ldist_ptime_da_rt same_region lat_diff, a(pcode1 pcode2)

* Neighbour Model
ppmlhdfe good_count ldist_ptime_da close_dist same_region lat_diff, a(pcode1 pcode2)

* Endowment Model
ppmlhdfe good_count ldist_ptime_da close_dist x_simdist same_region lat_diff, a(pcode1 pcode2)


** Graph non-linear relationship

generate dist_round=floor(ldist_ptime_da*15)/15
egen good_round=mean(good_count), by(dist_round)
egen tag=tag(dist_round)
egen count=count(dist_round), by(dist_round)
twoway lpolyci good_count ldist_ptime_da, lcolor(dknavy) bwidth(0.9) deg(1) ciplot(rline) alwidth(vthin) alpattern("-.") || scatter good_round dist_round, mcolor(dknavy) msize(tiny) msymbol(O) ytitle("Trade") xtitle("Distance") bgcolor("white") graphregion(color(white) margin(l-3 r+1)) scale(1.2) legend(off)


** Robustness

* product shares
ppmlhdfe good_share ldist_ptime_da close_dist x_simdist same_region lat_diff, a(pcode1 pcode2)

* Sequential drop of cities
ppmlhdfe good_count ldist_ptime_da close_dist x_simdist same_region lat_diff if (pcode1 != 254 & pcode2 != 254), a(pcode1 pcode2)

ppmlhdfe good_count ldist_ptime_da close_dist x_simdist same_region lat_diff if (pcode1 != 251 & pcode2 != 251), a(pcode1 pcode2)

ppmlhdfe good_count ldist_ptime_da close_dist x_simdist same_region lat_diff if (pcode1 != 651 & pcode2 != 651), a(pcode1 pcode2)

ppmlhdfe good_count ldist_ptime_da close_dist x_simdist same_region lat_diff if (pcode1 != 507 & pcode2 != 507), a(pcode1 pcode2)

ppmlhdfe good_count ldist_ptime_da close_dist x_simdist same_region lat_diff if (pcode1 != 506 & pcode2 != 506), a(pcode1 pcode2)

ppmlhdfe good_count ldist_ptime_da close_dist x_simdist same_region lat_diff if (pcode1 != 101 & pcode2 != 101), a(pcode1 pcode2)

ppmlhdfe good_count ldist_ptime_da close_dist x_simdist same_region lat_diff if (pcode1 != 103 & pcode2 != 103), a(pcode1 pcode2)



*****************************************************************************
*****************************************************************************



********************************
**# 3 Trade Analysis
********************************
clear

use trade_analysis_data.dta


**# 3.1 Variable construction
egen growth_30 = std(place_change_30)

* Controls
tabulate cent_lat, generate(lat_dummy_)
tabulate cent_lon, generate(lon_dummy_)
global cell_fe lat_dummy_* lon_dummy_*

tabulate region_con, generate(region_dummy_)

* Diversity indices
gen div_x = abs(hhi_x - 1)
gen div_m = abs(hhi_m - 1)

* Other variables
gen lnear_dist = ln(near_portcode_dist)

gen samp_dist = (near_portcode_dist <= 500)
gen robust1_dist = (near_portcode_dist <= 350)
gen robust2_dist = (near_portcode_dist <= 250)

* Distance weighting
gen weight_norm = 1/(near_portcode_dist)

gen w_div_x = weight_norm*div_x
gen w_div_m = weight_norm*div_m

gen w_mfg_x = weight_norm*mfg_share_x
gen w_spc_x = weight_norm*spc_share_x

gen w_gld_m = weight_norm*gld_share_m

gen w_mean_cent = weight_norm*index_mean_seadist_hr


**# 3.2 Regressions

reghdfe growth_30 w_mean_cent rome_emp region_dummy_* if land == 1 & samp_dist == 1, a(cent_lat cent_lon)

reghdfe growth_30 w_div_x w_div_m rome_emp region_dummy_* if land == 1 & samp_dist == 1, a(cent_lat cent_lon)

reghdfe growth_30 w_mfg_x w_spc_x w_gld_m rome_emp region_dummy_* if land == 1 & samp_dist == 1, a(cent_lat cent_lon)


** Robustness
* Change in sample distance
reghdfe growth_30 w_mean_cent rome_emp region_dummy_* if land == 1 & robust1_dist == 1, a(cent_lat cent_lon)

reghdfe growth_30 w_div_x w_div_m rome_emp region_dummy_* if land == 1 & robust1_dist == 1, a(cent_lat cent_lon)

reghdfe growth_30 w_mfg_x w_spc_x w_gld_m rome_emp region_dummy_* if land == 1 & robust1_dist == 1, a(cent_lat cent_lon)


reghdfe growth_30 w_mean_cent rome_emp region_dummy_* if land == 1 & robust2_dist == 1, a(cent_lat cent_lon)

reghdfe growth_30 w_div_x w_div_m rome_emp region_dummy_* if land == 1 & robust2_dist == 1, a(cent_lat cent_lon)

reghdfe growth_30 w_mfg_x w_spc_x w_gld_m rome_emp region_dummy_* if land == 1 & robust2_dist == 1, a(cent_lat cent_lon)


* Conley standard errors
acreg growth_30 w_mean_cent rome_emp region_dummy_* if land == 1 & samp_dist == 1, spatial latitude(cent_lat) longitude(cent_lon) dist(1500) pfe1(cent_lat) pfe2(cent_lon)

acreg growth_30 w_div_x w_div_m rome_emp region_dummy_* if land == 1 & samp_dist == 1, spatial latitude(cent_lat) longitude(cent_lon) dist(1500) pfe1(cent_lat) pfe2(cent_lon)

acreg growth_30 w_mfg_x w_spc_x w_gld_m rome_emp region_dummy_* if land == 1 & samp_dist == 1, spatial latitude(cent_lat) longitude(cent_lon) dist(1500) pfe1(cent_lat) pfe2(cent_lon)


**# 3.3 Third century decline
clear

use trade_analysis_data_third.dta


** Variable construction
egen growth_30 = std(place_change_30)

* Controls
tabulate cent_lat, generate(lat_dummy_)
tabulate cent_lon, generate(lon_dummy_)
global cell_fe lat_dummy_* lon_dummy_*

tabulate region_con, generate(region_dummy_)

* Diversity indices
gen div_x = abs(hhi_x - 1)
gen div_m = abs(hhi_m - 1)

* Other variables
gen lnear_dist = ln(near_portcode_dist)
gen samp_dist = (near_portcode_dist <= 500)

* Distance weighting
gen weight_norm = 1/(near_portcode_dist)

gen w_div_x = weight_norm*div_x
gen w_div_m = weight_norm*div_m

gen w_mfg_x = weight_norm*mfg_share_x
gen w_spc_x = weight_norm*spc_share_x

gen w_gld_m = weight_norm*gld_share_m

gen w_mean_cent = weight_norm*index_mean_seadist_hr


** Regressions
reghdfe growth_30 w_mean_cent rome_emp region_dummy_* if land == 1 & samp_dist == 1, a(cent_lat cent_lon)

reghdfe growth_30 w_div_x w_div_m rome_emp region_dummy_* if land == 1 & samp_dist == 1, a(cent_lat cent_lon)

reghdfe growth_30 w_mfg_x w_spc_x w_gld_m rome_emp region_dummy_* if land == 1 & samp_dist == 1, a(cent_lat cent_lon)

