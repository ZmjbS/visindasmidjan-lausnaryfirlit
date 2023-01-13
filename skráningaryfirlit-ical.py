# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 18:22:55 2019

@author: martin
"""

from datetime import datetime#, timedelta
import pandas as pd
#import numpy as np
#import re
import icalendar as ical, pytz
import math

#Nafnið á CSV skránni með skráningunum:
#filename = "Skráningar 2022-2023/IUB-2022.09.05.csv"
# Opnum nýjustu CSV skrána í réttri möppu:
import glob, os
list_of_files = glob.glob(os.getcwd()+"/Skráningar 2022-2023/*")
latest_file = max(list_of_files, key=os.path.getctime)

cal = ical.Calendar()
cal.add('prodid', '-//Dagatal Vísindasmiðjunnar//')
cal.add('version', '2.0')

cal_tue = ical.Calendar()
cal_tue.add('prodid', '-//Þriðjudagar í Vísindasmiðjunni//')
cal_tue.add('version', '2.0')
cal_wed = ical.Calendar()
cal_wed.add('prodid', '-//Miðvikudagar Vísindasmiðjunni//')
cal_wed.add('version', '2.0')
cal_thu = ical.Calendar()
cal_thu.add('prodid', '-//Fimmtudagar Vísindasmiðjunni//')
cal_thu.add('version', '2.0')
cal_fri = ical.Calendar()
cal_fri.add('prodid', '-//Föstudagar Vísindasmiðjunni//')
cal_fri.add('version', '2.0')


with open(latest_file, encoding='utf-8') as csv_file:
    # Import the CSV file into a Pandas dataframe
    df = pd.read_csv(csv_file)#, parse_dates=['Dags.', 'Frá', 'Til'], dayfirst=True)
    
    # Merge the split dates and times into a datetime
    df['hefst'] = pd.to_datetime(df['Dags.'] + ' ' + df['Frá'], dayfirst=True)
    df['lykur'] = pd.to_datetime(df['Dags.'] + ' ' + df['Til'], dayfirst=True)
    
    for index, data in df.iterrows():
        #print(type(data))
        event = ical.Event()
#        print(type(data['Athugasemdir']))
        #print(data['Athugasemdir'])
        if isinstance(data['Athugasemdir'],str):
            aths = "☆"
            event.add('aths', data['Athugasemdir'])
        else:
            aths = ""
            event.add('aths', '')
        event.add('summary', data['Skóli']+' - '+data['Bekkur']+' ('+str(data['Fjöldi'])+') - '+data['Tengiliður']+' ('+str(data['Sími'])+')'+' '+aths)
#        print(event['summary'])
        event.add('skoli', data['Skóli'])
        event.add('bekkur', data['Bekkur'])
        event.add('fjoldi', data['Fjöldi'])
        event.add('tengilidur', data['Tengiliður'])
        event.add('simi', data['Sími'])
        event.add('dtstart', data['hefst'])
        event.add('dtend', data['lykur'])
        
        print(event['dtstart'].dt, event['tengilidur'])
#        print(event.)
        cal.add_component(event)
        if event['dtstart'].dt.dayofweek == 1:
            cal_tue.add_component(event)
        else:
            if event['dtstart'].dt.dayofweek == 2:
                cal_wed.add_component(event)
            else:
                if event['dtstart'].dt.dayofweek == 3:
                    cal_thu.add_component(event)
                else:
                    if event['dtstart'].dt.dayofweek == 4:
                        cal_fri.add_component(event)
            
    # Open file to writing in binary mode
    outputfile = open(r"skraningar.ical", "wb")
    outputfile.write(cal.to_ical())
    outputfile.close()    

    # Open file to writing in binary mode
    outputfile = open(r"skraningar_þri.ical", "wb")
    outputfile.write(cal_tue.to_ical())
    outputfile.close()    

    # Open file to writing in binary mode
    outputfile = open(r"skraningar_mið.ical", "wb")
    outputfile.write(cal_wed.to_ical())
    outputfile.close()    

    # Open file to writing in binary mode
    outputfile = open(r"skraningar_fim.ical", "wb")
    outputfile.write(cal_thu.to_ical())
    outputfile.close()    

    # Open file to writing in binary mode
    outputfile = open(r"skraningar_fös.ical", "wb")
    outputfile.write(cal_fri.to_ical())
    outputfile.close()    

            
    csv_file.close()
