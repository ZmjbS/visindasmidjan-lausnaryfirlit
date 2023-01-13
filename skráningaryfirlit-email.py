# -*- coding: utf-8 -*-

import datetime
import pandas as pd
import numpy as np
import locale
locale.setlocale(locale.LC_TIME, "is_IS")

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

with open(r"Skráningar 2021-2022/IUB-2022.01.11.csv", encoding='utf-8') as csv_file:
    #csv_reader = csv.DictReader(csv_file, delimiter=',')
    df = pd.read_csv(csv_file)#, parse_dates=['Dags.', 'Frá', 'Til'], dayfirst=True)
    #print(df['Fjöldi'])# = df['Fjöldi'].astype(int)
    
    df['hefst'] = pd.to_datetime(df['Dags.'] + ' ' + df['Frá'], dayfirst=True)

#    print(df.dtypes)
    print("Fjöldi bókana: "+str(len(df)))

    sdf = df.sort_values('hefst')
    now = datetime.datetime.now()
    presentweek = now.isocalendar()[1]
    print(presentweek)
    
    # TODO: Athuga að þetta séu "réttar" vikur! (þ.e. réttur ISO staðall m.v. það sem er uppi á vegg.)
    weeknum = presentweek+1
    
    
    print('Vika númer ', str(weeknum))
    for d in sdf[(sdf['hefst'] > np.datetime64(datetime.datetime.strptime(str(now.year)+'-W'+str(weeknum)+'-1', "%Y-W%W-%w"))) & (sdf['hefst'] < np.datetime64(datetime.datetime.strptime(str(now.year)+'-W'+str(weeknum+1)+'-1', "%Y-W%W-%w")))].T:
        timi = df['hefst'][d].to_pydatetime()
        print(timi)
        print(int(df['Fjöldi'][d]), '(', df['Bekkur'][d], ')', df['Skóli'][d])
        print('"' + df['Tengiliður'][d] + '" <'+df['Netfang'][d]+'>')
        print('Heimsókn í Vísindasmiðju HÍ ' + timi.strftime("%d. %B %Y klukkan %H:%M"))
        if not pd.isna(df['Athugasemdir'][d]):
            print('\t'+ df['Athugasemdir'][d])

        print()
        print('Sæl '+ df['Tengiliður'][d].split(' ')[0] +',')
        print('Bara að minna á heimsókn ykkar í Vísindasmiðjuna:')
        print('  '+vikudaginn(int(timi.strftime("%w"))-1) + timi.strftime(" %d. %B klukkan %H:%M"))
        print('Þú getur fengið yfirlit yfir tíma sem hafa verið bókaðir á þínu netfangi hér:')
        print('  http://hi.lausn.is/IceUniBooking/swregedit?t='+df['Netfang'][d])
        print('Hlökkum til að sjá ykkur!')
        print('----------------------')
        
    outputfile = open(r"tölvupóstar_viku_"+str(weeknum)+".html", "w", encoding='utf-8')
    outputfile.write('<!doctype html>\n')
    outputfile.write('<html lang="en">\n')
    outputfile.write('<head>\n')
    outputfile.write('<!-- Required meta tags -->\n')
    outputfile.write('<meta charset="utf-8">\n')
    outputfile.write('<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">\n')
    outputfile.write('\n')
    
    import urllib.parse
    
    for d in sdf[(sdf['hefst'] > np.datetime64(datetime.datetime.strptime(str(now.year)+'-W'+str(weeknum)+'-1', "%Y-W%W-%w"))) & (sdf['hefst'] < np.datetime64(datetime.datetime.strptime(str(now.year)+'-W'+str(weeknum+1)+'-1', "%Y-W%W-%w")))].T:
        timi = df['hefst'][d].to_pydatetime()
#        print(timi)
#        print(int(df['Fjöldi'][d]), '(', df['Bekkur'][d], ')', df['Skóli'][d])
        mailto= '"'+ df['Tengiliður'][d] +'" <'+ df['Netfang'][d] +'>'
        subject='Heimsókn í Vísindasmiðju HÍ ' + timi.strftime("%d. %B %Y klukkan %H:%M")
        body = 'Sæl '+ df['Tengiliður'][d].split(' ')[0] +',\n\n'
        body += 'Bara að minna á heimsókn ykkar í Vísindasmiðjuna:\n'
        body +='  '+vikudaginn(int(timi.strftime("%w"))-1) + timi.strftime(" %d. %B klukkan %H:%M") +'\n\n'
        body +='Þú getur fengið yfirlit yfir tíma sem hafa verið bókaðir á þínu netfangi hér:\n'
        uri = 'http://hi.lausn.is/IceUniBooking/swregedit?t='+df['Netfang'][d]
        body +='  '+uri+'\n\n'
        body +='Hlökkum til að sjá ykkur!'
        
        outputfile.write('<div style="border: thin solid #949; margin: 0.5em;">')
        outputfile.write('<div style="color: gray; margin: 0.5em;">'+timi.strftime("%d. %B %H:%M")+'</div>')
        uri = 'http://hi.lausn.is/IceUniBooking/swregedit?t='+df['Netfang'][d]
        outputfile.write('<div style="margin: 0.5em;">  <a href="'+uri+'">'+uri+'</a></div>')
        outputfile.write('<div style="margin: 0.5em;"><a href=\'mailto:'+mailto+'?subject='+subject+'&body='+urllib.parse.quote(body)+'\'>'+ df['Tengiliður'][d] +'</a></div>')
        outputfile.write('<div style="margin: 0.5em;">'+df['Bekkur'][d] +' '+ df['Skóli'][d]+'</div>')
        if not pd.isna(df['Athugasemdir'][d]):
            outputfile.write('<p style="font-weight: bold">'+ df['Athugasemdir'][d]+'</p>')

        outputfile.write('\n')
        #outputfile.write('<p>Sæl '+ df['Tengiliður'][d].split(' ')[0] +',</p>')
        #outputfile.write('<p>Bara að minna á heimsókn ykkar í Vísindasmiðjuna:<br />')
        #outputfile.write('  '+vikudaginn(int(timi.strftime("%w"))-1) + timi.strftime(" %d. %B klukkan %H:%M") +'</p>')
        #outputfile.write('<p>Þú getur fengið yfirlit yfir tíma sem hafa verið bókaðir á þínu netfangi hér:<br />')
        outputfile.write('</div>')
        #outputfile.write('<p>Hlökkum til að sjá ykkur!</p>')
        
    outputfile.write('</html>')
    outputfile.close()

    csv_file.close()