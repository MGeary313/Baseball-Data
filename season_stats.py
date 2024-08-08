import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

teams = [
    'angels', 'astros', 'athletics', 'bluejays', 'braves', 'brewers', 'cardinals', 'cubs', 
    'dbacks', 'dodgers', 'giants', 'guardians', 'marlins', 'mariners', 'mets', 'nationals', 
    'orioles', 'padres', 'phillies', 'pirates', 'rangers', 'rays', 'reds', 'redsox', 
    'rockies', 'royals', 'tigers', 'twins', 'whitesox', 'yankees'
]

# Function to clean player names
def clean_player_name(name):
    # Remove digits and special characters
    name = re.sub(r'\d+', '', name)  # Remove digits
    name = re.sub(r'[^\w\s]', '', name)  # Remove special characters
    name = re.sub(r'\s+', ' ', name)  # Replace multiple spaces with a single space
    
    # Split the name into parts
    name_parts = re.findall(r'[A-Z][a-z]*', name)  # Match capital letters followed by lowercase letters
    
    # Join the cleaned parts
    cleaned_name = ' '.join(name_parts[:3])
    
    return cleaned_name.strip()

# Collect all player data
all_players_data = []

# Create an Excel writer object
with pd.ExcelWriter('mlb_stats.xlsx') as writer:
    for team in teams:
        url = f"https://www.mlb.com/{team}/stats"

        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the page content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the table containing the stats
            table = soup.find('table', {'class': 'bui-table'})
            
            # Check if the table is found
            if table:
                # Manually define the headers to ensure they match the data columns
                headers = [
                    'PLAYER', 'TEAM', 'G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 
                    'BB', 'SO', 'SB', 'CS', 'AVG', 'OBP', 'SLG', 'OPS'
                ]
                #print(f"Number of headers: {len(headers)}")
                #print("Headers:", headers)
                
                # Extract table rows
                rows = []
                for row in table.find_all('tr'):
                    columns = row.find_all('td')
                    if columns:
                        player_name = row.find('th').text.strip()  # Extract player name from 'th' element
                        player_name = clean_player_name(player_name)  # Clean the player name
                        row_data = [player_name] + [column.text.strip() for column in columns]
                        rows.append(row_data)
                        all_players_data.append(row_data)  # Add to the combined list
                        #print(f"Row length: {len(row_data)}, Row data: {row_data}")
                
                # Filter out rows that do not match the number of headers
                valid_rows = [row for row in rows if len(row) == len(headers)]
                
                # Create a DataFrame
                df = pd.DataFrame(valid_rows, columns=headers)
                
                # Write the DataFrame to a specific sheet in the Excel file
                df.to_excel(writer, sheet_name=team, index=False)
                print(f"Data for the {team.title()} has been written to the spreadsheet.")
            else:
                print(f"No table found on the page for the {team.title()}")
        else:
            print(f"Failed to retrieve the page for the {team.title()}. Status code: {response.status_code}")
    
    # Create a DataFrame for all players combined
    all_players_df = pd.DataFrame(all_players_data, columns=headers)
    
    # Write the combined DataFrame to the first sheet in the Excel file
    all_players_df.to_excel(writer, sheet_name='All Players', index=False)
    print("All player data has been written to the 'All Players' sheet.")

print("All data has been written to 'mlb_stats.xlsx'")
