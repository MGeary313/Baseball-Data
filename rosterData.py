import requests
from bs4 import BeautifulSoup
import pandas as pd

teams = ['dbacks',
         'braves',
         'orioles',
         'redsox', 
         'cubs',
         'whitesox',
         'reds',
         'guardians',
         'rockies',
         'tigers',
         'astros',
         'royals',
         'angels',
         'dodgers',
         'marlins',
         'brewers',
         'twins',
         'mets',
         'yankees',
         'athletics',
         'phillies',
         'pirates',
         'padres',
         'giants',
         'mariners',
         'cardinals',
         'rays',
         'rangers',
         'bluejays',
         'nationals'
         ]

# Initialize a dictionary to hold dataframes for each team
team_rosters = {}

for team in teams:
    url = f"https://www.mlb.com/{team}/roster/40-man"
    #print(url)

    response = requests.get(url)
    #print(response)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        roster_div = soup.find('div', class_='players')
        if roster_div:
            roster_tables = roster_div.find_all('table', class_='roster__table')
            players_list = []
            #print(team)
            #print('-------------')
            for roster_table in roster_tables:
                players = roster_table.find('tbody').find_all('tr')
                for player in players:
                    found_player = player.find('td', class_='info').find('a')
                    if found_player:
                        player_name = found_player.string
                        players_list.append(player_name)
                        #print(player_name)
            # Create a dataframe for the team
            team_rosters[team] = pd.DataFrame(players_list, columns=['Player'])
    else:
        print(f"Failed to retrieve data for {team}, status code: {response.status_code}")

# Write the dataframes to an Excel file with each team in a separate sheet
with pd.ExcelWriter('mlb_rosters.xlsx') as writer:
    for team, roster_df in team_rosters.items():
        roster_df.to_excel(writer, sheet_name=team, index=False)

print("Rosters have been saved to mlb_rosters.xlsx")
