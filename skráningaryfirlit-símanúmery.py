# -*- coding: utf-8 -*-

import datetime
import pandas as pd
import numpy as np
import locale
locale.setlocale(locale.LC_TIME, "is_IS")

#Nafnið á CSV skránni með skráningunum:
#filename = "Skráningar 2022-2023/IUB-2022.09.05.csv"
# Opnum nýjustu CSV skrána í réttri möppu:
import glob, os
list_of_files = glob.glob(os.getcwd()+"/Skráningar 2022-2023/*csv")
latest_file = max(list_of_files, key=os.path.getctime)

# Velja vikuna sem prenta á út. +1 gefur næstu viku.
offset = +1

def vikudaginn(n):
#    print('in vikudaginn the type is',type(n))
#    print(n)
    if n == 1:
        return 'þriðjudaginn'
    else:
        if n == 2:
            return 'miðvikudaginn'
        else:
            if n == 3:
                return 'fimmtudaginn'
            else:
                if n == 4:
                    return 'föstudaginn'
                else:
                    return None

with open(latest_file, encoding='utf-8') as csv_file:
    df = pd.read_csv(csv_file)#, parse_dates=['Dags.', 'Frá', 'Til'], dayfirst=True)
    
    df['hefst'] = pd.to_datetime(df['Dags.'] + ' ' + df['Frá'], dayfirst=True)


    sdf = df.sort_values('hefst')
    now = datetime.datetime.now()
    presentweek = now.isocalendar()[1]
    #print(presentweek)
    
    # Velja vikuna sem prenta á út. +1 gefur næstu viku.
    weeknum = presentweek+offset
    
    
    print('Vika númer ', str(weeknum))
    for d in sdf[(sdf['hefst'] > np.datetime64(datetime.datetime.strptime(str(now.year)+'-W'+str(weeknum)+'-1', "%Y-W%W-%w"))) & (sdf['hefst'] < np.datetime64(datetime.datetime.strptime(str(now.year)+'-W'+str(weeknum+1)+'-1', "%Y-W%W-%w")))].T:
        timi = df['hefst'][d].to_pydatetime()
        print('---- ', timi.strftime("%A") ,' -----------------------')
        print(timi.strftime("%H:%M - %d. %B %Y"))
        print(df['Tengiliður'][d] + ' ('+df['Sími'][d]+')')
        print(int(df['Fjöldi'][d]), '(', df['Bekkur'][d], ')', df['Skóli'][d])
        if not pd.isna(df['Athugasemdir'][d]):
            print('\t'+ df['Athugasemdir'][d])
        
    print('=== Vika nr. ', weeknum ,'=================================')
    for d in sdf[(sdf['hefst'] > np.datetime64(datetime.datetime.strptime(str(now.year)+'-W'+str(weeknum)+'-1', "%Y-W%W-%w"))) & (sdf['hefst'] < np.datetime64(datetime.datetime.strptime(str(now.year)+'-W'+str(weeknum+1)+'-1', "%Y-W%W-%w")))].T:
        timi = df['hefst'][d].to_pydatetime()
        print(timi.strftime("%A %d. %B"))
        print(df['hefst'][d].strftime('%H:%M'), ' - ', df['Skóli'][d], ', ', df['Bekkur'][d], ' (', int(df['Fjöldi'][d]), ' nem)')
              
 
    csv_file.close()