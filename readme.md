
Sample call: 
'''python

import datetime as dt

montereyBayBouysIds =  {"MBARI_M1" : 46092,
                    "OffShore_wave" :46114,
                    "OffShore_ares" :46042,
                    "Canyon_wave" :46236,
                    "Hopkines_wave" : 46240,
                    }
bouy = montereyBayBouysIds['MBARI_M1']                        
startDate = dt.datetime(2015,1,1)
data = get_nc_dods(startDate,endDate=dt.datetime(2015,12,1),nbdcId=bouy)
'''