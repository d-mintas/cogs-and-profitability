wrt.train <-
  wrt.train %>%
    transmute(runtime=runTime,
              isAuto = -1 * (stationTypeId - 2)
              qty = qtyPerTab,
              totImps=tot_imps_per_tab,
              maxInks = maxInksPerTab,
              totInks = totInksPerTab,
              locs = dopasPerTab,
              gini = gini);
