# -*- coding: utf-8 -*-

import datetime
import pandas as pd
import numpy as np
import re
import locale
locale.setlocale(locale.LC_TIME, "is_IS")

outputfile = open(r"Skráningar 2022-2023/index.html", "w", encoding='utf-8')

#Nafnið á CSV skránni með skráningunum:
#filename = "Skráningar 2022-2023/IUB-2022.09.05.csv"
# Opnum nýjustu CSV skrána í réttri möppu:
import glob, os
list_of_files = glob.glob(os.getcwd()+"/Skráningar 2022-2023/*csv")
latest_file = max(list_of_files, key=os.path.getctime)

def odd_or_even_month(dt):
    # Return whether the month number is odd or even.
    return int(dt.strftime("%m")) % 2

with open(latest_file, encoding='utf-8') as csv_file:
    #csv_reader = csv.DictReader(csv_file, delimiter=',')
    df = pd.read_csv(csv_file)#, parse_dates=['Dags.', 'Frá', 'Til'], dayfirst=True)
    #print(df['Fjöldi'])# = df['Fjöldi'].astype(int)
    
    df['hefst'] = pd.to_datetime(df['Dags.'] + ' ' + df['Frá'], dayfirst=True)

    print(df.dtypes)

    sdf = df.sort_values('hefst')
    now = datetime.datetime.now()
    presentweek = now.isocalendar()[1]
    print(presentweek)
    
    html = '''
    <!doctype html>
    <html lang="en">
    <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.4/popper.min.js"></script>
    <style>
    table { border-collapse: separate; border-spacing: 2px; }
    td { background-color: #fafafa; border-top: 1px solid #ccc; height: 2em; vertical-align: top; }
    th.weeknum_head { width: 3em; }
    th.weeknum { font-size: 3em; color: #aaa; }
    th.dayname, td { width: 14%; }
    td.jafntolumanudur { background-color: #eee; }
    td.oddatolumanudur { background-color: #fff; }
    td div { width: calc(100%-2em);  }
    
    .timi { background-color: #ae9; border-radius: 0.4em; margin: 3px; padding: 0 3px; }
    .timi { color: #226088; }
    X.timi.aths { color: #FFD700; }
    .timi.aths { position: relative; border-bottom: 1px dotted black; /* If you want dots under the hoverable text */ }
    .timi .tooltp { visibility: hidden; background-color: black; color: #fff; text-align: center; padding: 5px 0; border-radius: 6px; /* Position the tooltip text - see examples below! */ position: absolute; z-index: 1; }
    .timi:hover .tooltp { visibility: visible; }
    .timi .tooltp { top: calc(100% + .5em); }
    .timi .tooltp::after { content: " "; position: absolute; bottom: 100%;  /* At the top of the tooltip */  left: 50%;  margin-left: -5px; border-width: 5px;  border-style: solid;  border-color: transparent transparent black transparent;}
    </style>
    </head>
    <body>
    <h1 style="text-align: center">Vísindasmiðjan vorið 2023</h1>
    '''.strip()
    
    outputfile.write(html)
    outputfile.write('<table>\n')
    outputfile.write('<tr>\n')
    outputfile.write('<th class="weeknum_head">Vika</th>')
    for weekday in [1,2,3,4,5,6,0]:
        outputfile.write('\t<th class="dayname">'+datetime.datetime.strptime(str(now.year)+'-W2-'+str(weekday), "%Y-W%W-%w").strftime("%A")+'</th>\n')
    outputfile.write('</tr>\n')
    
    for weeknum in range(1, 20):
        print('Vika númer ', str(weeknum))
        outputfile.write('<tr id="vika-'+str(weeknum)+'">\n')
        outputfile.write('<th class="weeknum">'+str(weeknum)+'</th>')
        for weekday in [1,2,3,4,5,6,0]:
            dagur_hefst = datetime.datetime.strptime(str(now.year)+'-W'+str(weeknum)+'-'+str(weekday), "%Y-W%W-%w")
            dagur_lykur = dagur_hefst + datetime.timedelta(days=1)
            print(dagur_hefst.strftime("%A"))
            if odd_or_even_month(dagur_hefst) == 0:
                outputfile.write('<td class="dagur jafntolumanudur">')
            else:
                outputfile.write('<td class="dagur oddatolumanudur">')
            outputfile.write('<div class="dagsetning">'+dagur_hefst.strftime("%d"))
            for d in sdf[(sdf['hefst'] > np.datetime64(dagur_hefst)) & (sdf['hefst'] < np.datetime64(dagur_lykur))].T:
                print(df['hefst'][d], '\t', int(df['Fjöldi'][d]), '(', df['Bekkur'][d], ')', df['Skóli'][d], '\t (', df['Tengiliður'][d], ')')
                if not pd.isna(df['Athugasemdir'][d]):
                    print('\t'+ df['Athugasemdir'][d])
                    athsclass = " aths"
                    tooltip = df['Athugasemdir'][d] + '\n'
                else:
                    athsclass = ""
                    tooltip = ""
#                tooltip += df['Skóli'][d] + ' ['+ df['Tengiliður'][d] +']'
                #outputfile.write('\t<div class="timi'+athsclass+'"><a href="#" data-toggle="tooltip" data-placement="top" title="'+tooltip+'">\n')
                outputfile.write('\t<div class="timi'+athsclass+'">\n')
                if tooltip != "":
                    outputfile.write('<span class="tooltp">'+tooltip+'</span>')
                timi_text = '<strong>{hefst}</strong> {skoli} {bekkur} b ({fjoldi})<br>{tengilidur} ({simi})'.format(
                    hefst=sdf['hefst'][d].strftime('%H:%M'),
                    skoli=df['Skóli'][d],
                    bekkur=str(re.search('[0-9][^ ]*',df['Bekkur'][d]).group(0)),
                    fjoldi=df['Fjöldi'][d],
                    tengilidur=df['Tengiliður'][d],
                    simi=df['Sími'][d])
                
#                outputfile.write(''+str(sdf['hefst'][d].strftime('%H:%M'))+'')
#                outputfile.write(' <strong>'+str(df['Fjöldi'][d])+' ('+' bekkur)</strong><br>\n')
#                outputfile.write(df['Skóli'][d] + '<br> ['+ df['Tengiliður'][d] +'('+str(df['Sími'][d])+')]</div>\n')
                outputfile.write(timi_text)
                #outputfile.write()
                outputfile.write('</div>')
            outputfile.write('</td>')
        outputfile.write('</tr>')
        print()

    outputfile.write('</table>')
    outputfile.write('</html>')
            
    csv_file.close()
    outputfile.close()