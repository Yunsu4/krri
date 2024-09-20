import pandas as pd
from model.Line1_4_riders import Line1_riders, Line4_riders




def R1_controller(month, dow, time):

    riders1= Line1_riders(month, dow, time)
    riders1.rename(columns={'승차인원': '승차인원_1', '하차인원': '하차인원_1'}, inplace=True)

    riders4= Line4_riders(month, dow, time)
    riders4.rename(columns={'승차인원': '승차인원_4', '하차인원': '하차인원_4'}, inplace=True)


    merged_data = pd.merge(riders1, riders4, on=['month', 'dow', 'hour', 'exit'], how='inner')

    return merged_data



    

    





        
