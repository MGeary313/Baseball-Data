import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the MLB starting lineups page
url = 'https://www.mlb.com/starting-lineups'

# Send a request to fetch the webpage
response = requests.get(url)
response.raise_for_status()  # Ensure we got a successful response

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find the sections containing the lineups
games = soup.find_all('div', class_='starting-lineups__teams')

# Debugging: print the number of games found
print(f"Number of games found: {len(games)}")

# Prepare a list to hold all the data
data = []

# Iterate through each game section and extract lineups
for game in games:
    # Extract team headers
    team_headers = game.find('div', class_='starting-lineups__teams--header')
    if team_headers:
        away_team = team_headers.find('div', class_='starting-lineups__teams--away-head').text.strip()
        home_team = team_headers.find('div', class_='starting-lineups__teams--home-head').text.strip()
        
        # Debugging: print the team names
        print(f"Away Team: {away_team}, Home Team: {home_team}")
    
        # Extract away team players
        away_team_list = game.find('ol', class_='starting-lineups__team--away')
        if away_team_list:
            away_players = away_team_list.find_all('a', class_='starting-lineups__player--link')
            for player in away_players:
                player_name = player.text.strip()
                data.append([away_team, player_name])
        
        # Extract home team players
        home_team_list = game.find('ol', class_='starting-lineups__team--home')
        if home_team_list:
            home_players = home_team_list.find_all('a', class_='starting-lineups__player--link')
            for player in home_players:
                player_name = player.text.strip()
                data.append([home_team, player_name])

# Remove duplicates from data
unique_data = []
seen_entries = set()
for entry in data:
    if tuple(entry) not in seen_entries:
        seen_entries.add(tuple(entry))
        unique_data.append(entry)

# Print the data to check if it is being extracted correctly
for entry in unique_data:
    print(entry)

# Create a DataFrame from the extracted data
df = pd.DataFrame(unique_data, columns=['Team', 'Player'])

# Save the DataFrame to an Excel file
df.to_excel('mlb_starting_lineups.xlsx', index=False)

print("Data saved to mlb_starting_lineups.xlsx")
