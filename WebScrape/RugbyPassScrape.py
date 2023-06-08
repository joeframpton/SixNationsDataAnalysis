import csv
import requests
import time
from bs4 import BeautifulSoup
from lxml import etree


def write_line(output): 
    with open('sixnationsstats.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(output)

URLS_BY_YEAR = {
    2015:['https://www.rugbypass.com/live/england-vs-wales/stats/?g=915011',
'https://www.rugbypass.com/live/ireland-vs-italy/stats/?g=915012',
'https://www.rugbypass.com/live/france-vs-scotland/stats/?g=915013',
'https://www.rugbypass.com/live/england-vs-italy/stats/?g=915021',
'https://www.rugbypass.com/live/france-vs-ireland/stats/?g=915022',
'https://www.rugbypass.com/live/scotland-vs-wales/stats/?g=915023',
'https://www.rugbypass.com/live/italy-vs-scotland/stats/?g=915031',
'https://www.rugbypass.com/live/france-vs-wales/stats/?g=915032',
'https://www.rugbypass.com/live/england-vs-ireland/stats/?g=915033',
'https://www.rugbypass.com/live/ireland-vs-wales/stats/?g=915041',
'https://www.rugbypass.com/live/england-vs-scotland/stats/?g=915042',
'https://www.rugbypass.com/live/france-vs-italy/stats/?g=915043',
'https://www.rugbypass.com/live/italy-vs-wales/stats/?g=915051',
'https://www.rugbypass.com/live/ireland-vs-scotland/stats/?g=915052',
'https://www.rugbypass.com/live/england-vs-france/stats/?g=915053',], 
    2016:['https://www.rugbypass.com/live/france-vs-italy/stats/?g=916011',
'https://www.rugbypass.com/live/england-vs-scotland/stats/?g=916012',
'https://www.rugbypass.com/live/ireland-vs-wales/stats/?g=916013',
'https://www.rugbypass.com/live/france-vs-ireland/stats/?g=916021',
'https://www.rugbypass.com/live/scotland-vs-wales/stats/?g=916022',
'https://www.rugbypass.com/live/england-vs-italy/stats/?g=916023',
'https://www.rugbypass.com/live/france-vs-wales/stats/?g=916031',
'https://www.rugbypass.com/live/italy-vs-scotland/stats/?g=916032',
'https://www.rugbypass.com/live/england-vs-ireland/stats/?g=916033',
'https://www.rugbypass.com/live/ireland-vs-italy/stats/?g=916041',
'https://www.rugbypass.com/live/england-vs-wales/stats/?g=916042',
'https://www.rugbypass.com/live/france-vs-scotland/stats/?g=916043',
'https://www.rugbypass.com/live/italy-vs-wales/stats/?g=916051',
'https://www.rugbypass.com/live/ireland-vs-scotland/stats/?g=916052',
'https://www.rugbypass.com/live/england-vs-france/stats/?g=916053'],
    2017:['https://www.rugbypass.com/live/ireland-vs-scotland/stats/?g=917011'
'https://www.rugbypass.com/live/england-vs-france/stats/?g=917012',
'https://www.rugbypass.com/live/italy-vs-wales/stats/?g=917013',
'https://www.rugbypass.com/live/ireland-vs-italy/stats/?g=917021',
'https://www.rugbypass.com/live/england-vs-wales/stats/?g=917022',
'https://www.rugbypass.com/live/france-vs-scotland/stats/?g=917023',
'https://www.rugbypass.com/live/scotland-vs-wales/stats/?g=917031',
'https://www.rugbypass.com/live/france-vs-ireland/stats/?g=917032',
'https://www.rugbypass.com/live/england-vs-italy/stats/?g=917033',
'https://www.rugbypass.com/live/ireland-vs-wales/stats/?g=917041',
'https://www.rugbypass.com/live/france-vs-italy/stats/?g=917042',
'https://www.rugbypass.com/live/england-vs-scotland/stats/?g=917043',
'https://www.rugbypass.com/live/italy-vs-scotland/stats/?g=917051',
'https://www.rugbypass.com/live/france-vs-wales/stats/?g=917052',
'https://www.rugbypass.com/live/england-vs-ireland/stats/?g=917053'
],
    2018:['https://www.rugbypass.com/live/scotland-vs-wales/stats/?g=918011',
'https://www.rugbypass.com/live/france-vs-ireland/stats/?g=918012',
'https://www.rugbypass.com/live/england-vs-italy/stats/?g=918013',
'https://www.rugbypass.com/live/ireland-vs-italy/stats/?g=918021',
'https://www.rugbypass.com/live/england-vs-wales/stats/?g=918022',
'https://www.rugbypass.com/live/france-vs-scotland/stats/?g=918023',
'https://www.rugbypass.com/live/france-vs-italy/stats/?g=918031',
'https://www.rugbypass.com/live/ireland-vs-wales/stats/?g=918032',
'https://www.rugbypass.com/live/england-vs-scotland/stats/?g=918033',
'https://www.rugbypass.com/live/ireland-vs-scotland/stats/?g=918041',
'https://www.rugbypass.com/live/england-vs-france/stats/?g=918042',
'https://www.rugbypass.com/live/italy-vs-wales/stats/?g=918043',
'https://www.rugbypass.com/live/italy-vs-scotland/stats/?g=918051',
'https://www.rugbypass.com/live/england-vs-ireland/stats/?g=918052',
'https://www.rugbypass.com/live/france-vs-wales/stats/?g=918053'
],
    2019:['https://www.rugbypass.com/live/france-vs-wales/stats/?g=919011',
'https://www.rugbypass.com/live/italy-vs-scotland/stats/?g=919012',
'https://www.rugbypass.com/live/england-vs-ireland/stats/?g=919013',
'https://www.rugbypass.com/live/ireland-vs-scotland/stats/?g=919021',
'https://www.rugbypass.com/live/italy-vs-wales/stats/?g=919022',
'https://www.rugbypass.com/live/england-vs-france/stats/?g=919023',
'https://www.rugbypass.com/live/france-vs-scotland/stats/?g=919031',
'https://www.rugbypass.com/live/england-vs-wales/stats/?g=919032',
'https://www.rugbypass.com/live/ireland-vs-italy/stats/?g=919033',
'https://www.rugbypass.com/live/scotland-vs-wales/stats/?g=919041',
'https://www.rugbypass.com/live/england-vs-italy/stats/?g=919042',
'https://www.rugbypass.com/live/france-vs-ireland/stats/?g=919043',
'https://www.rugbypass.com/live/france-vs-italy/stats/?g=919051',
'https://www.rugbypass.com/live/ireland-vs-wales/stats/?g=919052',
'https://www.rugbypass.com/live/england-vs-scotland/stats/?g=919053'],
    2020:['https://www.rugbypass.com/live/italy-vs-wales/stats/?g=20200201108818',
'https://www.rugbypass.com/live/ireland-vs-scotland/stats/?g=20200201108808',
'https://www.rugbypass.com/live/england-vs-france/stats/?g=20200202108806',
'https://www.rugbypass.com/live/ireland-vs-wales/stats/?g=20200208108808',
'https://www.rugbypass.com/live/england-vs-scotland/stats/?g=20200208108814',
'https://www.rugbypass.com/live/france-vs-italy/stats/?g=20200209108806',
'https://www.rugbypass.com/live/italy-vs-scotland/stats/?g=20200222108809',
'https://www.rugbypass.com/live/france-vs-wales/stats/?g=20200222108818',
'https://www.rugbypass.com/live/england-vs-ireland/stats/?g=20200223108804',
'https://www.rugbypass.com/live/england-vs-wales/stats/?g=20200307108804',
'https://www.rugbypass.com/live/france-vs-scotland/stats/?g=20200308108814',
'https://www.rugbypass.com/live/ireland-vs-italy/stats/?g=20200307108808',
'https://www.rugbypass.com/live/scotland-vs-wales/stats/?g=20200314108818',
'https://www.rugbypass.com/live/england-vs-italy/stats/?g=20200314108809',
'https://www.rugbypass.com/live/france-vs-ireland/stats/?g=20200314108806'],
    2021:[],
    2022:[],
    2023:['https://www.rugbypass.com/live/ireland-vs-wales/stats/?g=931169',
'https://www.rugbypass.com/live/england-vs-scotland/stats/?g=931170',
'https://www.rugbypass.com/live/france-vs-italy/stats/?g=931171',
'https://www.rugbypass.com/live/france-vs-ireland/stats/?g=931172',
'https://www.rugbypass.com/live/scotland-vs-wales/stats/?g=931173',
'https://www.rugbypass.com/live/england-vs-italy/stats/?g=931174',
'https://www.rugbypass.com/live/ireland-vs-italy/stats/?g=931175',
'https://www.rugbypass.com/live/england-vs-wales/stats/?g=931176',
'https://www.rugbypass.com/live/france-vs-scotland/stats/?g=931177',
'https://www.rugbypass.com/live/italy-vs-wales/stats/?g=931178',
'https://www.rugbypass.com/live/england-vs-france/stats/?g=931179',
'https://www.rugbypass.com/live/ireland-vs-scotland/stats/?g=931180',
'https://www.rugbypass.com/live/italy-vs-scotland/stats/?g=931181',
'https://www.rugbypass.com/live/france-vs-wales/stats/?g=931182',
'https://www.rugbypass.com/live/england-vs-ireland/stats/?g=931183'],
}


team1_xml_paths = {
    'team': '/html/body/main/section[1]/div[3]/div/div/div[1]/div',
    'score': '/html/body/main/section[1]/div[3]/div/div/div[2]/div/div[1]/span[1]', 
    'penalties': '//*[@id="statsSummary_stats"]/div[1]/div[2]',
    'tries': '//*[@id="statsSummary_stats"]/div[2]/div[2]',
    'conversions': '//*[@id="statsSummary_stats"]/div[3]/div[2]',
    'dropgoals': '//*[@id="statsSummary_stats"]/div[4]/div[2]',
    'territory%': '//*[@id="territory_stats"]/div[2]/div[2]/div[2]',
    'possession%': '//*[@id="possession_stats"]/div[5]/div[2]/div[2]',
    '22entries': '//*[@id="entries22_stats"]/div[1]/div[2]',
    'points_scored_per_entry': '//*[@id="entries22_stats"]/div[1]/div[2]',
    'scrums': '//*[@id="setPlays_stats"]/div[1]/div[2]',
    'scrums_won%': '//*[@id="setPlays_stats"]/div[2]/div[2]',
    'lineouts': '//*[@id="setPlays_stats"]/div[3]/div[2]',
    'lineouts_won%': '//*[@id="setPlays_stats"]/div[4]/div[2]',
    'restarts_received': '//*[@id="setPlays_stats"]/div[5]/div[2]',
    'restarts_won%': '//*[@id="setPlays_stats"]/div[6]/div[2]',
    'passes': '//*[@id="attack_stats"]/div[1]/div[2]',
    'carries': '//*[@id="attack_stats"]/div[2]/div[2]',
    'metres_after_contact': '//*[@id="attack_stats"]/div[3]/div[2]',
    'linebreaks': '//*[@id="attack_stats"]/div[4]/div[2]',
    'to_won': '//*[@id="turnovers_stats"]/div[1]/div[2]',
    'to_lost': '//*[@id="turnovers_stats"]/div[2]/div[2]',
    'penalties_conceded': '//*[@id="penalties_stats"]/div[1]/div[2]',
    'yellow_cards': '//*[@id="penalties_stats"]/div[2]/div[2]',
    'red_cards': '//*[@id="penalties_stats"]/div[3]/div[2]',
    'tackles_made': '//*[@id="defence_stats"]/div[1]/div[2]',
    'tackles_missed': '//*[@id="defence_stats"]/div[2]/div[2]',
    'tackle_success_rate%': '//*[@id="defence_stats"]/div[3]/div[2]',
    'kicks': '//*[@id="kicks_stats"]/div[1]/div[2]',
    'kick_ratio': '//*[@id="kicks_stats"]/div[2]/div[2]'
}

team2_xml_paths = {
    'team': '/html/body/main/section[1]/div[3]/div/div/div[3]/div',
    'score': '/html/body/main/section[1]/div[3]/div/div/div[2]/div/div[1]/span[2]',
    'penalties': '//*[@id="statsSummary_stats"]/div[1]/div[4]',
    'tries': '//*[@id="statsSummary_stats"]/div[2]/div[4]',
    'conversions': '//*[@id="statsSummary_stats"]/div[3]/div[4]',
    'dropgoals': '//*[@id="statsSummary_stats"]/div[4]/div[4]',
    'territory%': '//*[@id="territory_stats"]/div[2]/div[2]/div[4]',
    'possession%': '//*[@id="possession_stats"]/div[5]/div[2]/div[4]',
    '22entries': '//*[@id="entries22_stats"]/div[4]/div[1]',
    'points_scored_per_entry': '//*[@id="entries22_stats"]/div[3]/div[2]',
    'scrums': '//*[@id="setPlays_stats"]/div[1]/div[4]',
    'scrums_won%': '//*[@id="setPlays_stats"]/div[2]/div[4]',
    'lineouts': '//*[@id="setPlays_stats"]/div[3]/div[4]',
    'lineouts_won%': '//*[@id="setPlays_stats"]/div[4]/div[4]',
    'restarts_received': '//*[@id="setPlays_stats"]/div[5]/div[4]',
    'restarts_won%': '//*[@id="setPlays_stats"]/div[6]/div[4]',
    'passes': '//*[@id="attack_stats"]/div[1]/div[4]',
    'carries': '//*[@id="attack_stats"]/div[2]/div[4]',
    'metres_after_contact': '//*[@id="attack_stats"]/div[3]/div[4]',
    'linebreaks': '//*[@id="attack_stats"]/div[4]/div[4]',
    'to_won': '//*[@id="turnovers_stats"]/div[1]/div[4]',
    'to_lost': '//*[@id="turnovers_stats"]/div[2]/div[4]',
    'penalties_conceded': '//*[@id="penalties_stats"]/div[1]/div[4]',
    'yellow_cards': '//*[@id="penalties_stats"]/div[2]/div[4]',
    'red_cards': '//*[@id="penalties_stats"]/div[3]/div[4]',
    'tackles_made': '//*[@id="defence_stats"]/div[1]/div[4]',
    'tackles_missed': '//*[@id="defence_stats"]/div[2]/div[4]',
    'tackle_success_rate%': '//*[@id="defence_stats"]/div[3]/div[4]',
    'kicks': '//*[@id="kicks_stats"]/div[1]/div[4]',
    'kick_ratio': '//*[@id="kicks_stats"]/div[2]/div[4]'
}

stats_with_non_numbers = ['territory%', 'possession%', 'scrums_won%', 'lineouts_won%', 'restarts_won%', 'metres_after_contact', 'tackle_success_rate%'  ]

for year, URLS in URLS_BY_YEAR.items():
    for URL in URLS:
        
        webpage = requests.get(URL)
        soup = BeautifulSoup(webpage.content, 'html.parser')
        dom = etree.HTML(str(soup))

        team1_output = ['home']
        team2_output = ['away']

        for stat_name, xpath in team1_xml_paths.items():
            try:
                stat = dom.xpath(xpath)[0].text
                if stat_name in stats_with_non_numbers:
                    stat = ''.join(char for char in stat if char.isdigit())
                elif stat_name == 'kick_ratio':
                    stat = round(1/float(str(stat)[2:])*100, 3)
                team1_output.append(stat)
            except:
                team1_output.append(None)


        for stat_name, xpath in team2_xml_paths.items():
            try: 
                stat = dom.xpath(xpath)[0].text
                if stat_name in stats_with_non_numbers:
                    stat = ''.join(char for char in stat if char.isdigit())
                elif stat_name == 'kick_ratio':
                    stat = round(1/float(str(stat)[2:])*100, 3)
                team2_output.append(stat)
            except:
                team2_output.append(None)

        write_line([year]+team1_output+team2_output)
        write_line([year]+team2_output+team1_output)
        time.sleep(1)
    print('Finished year: ' + str(year))  