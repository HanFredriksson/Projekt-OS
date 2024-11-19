"""
Here we keep all the code that runs the dashboard, creats the graphs and handels the data from
the data calss.
The functions for what the graphs needs to show can be made here
Remeber there is a filter funktion built in the FetchOSData to make a general filtration of the data.
"""

from FetchOSData import OsDataFetcher
import dash

# The variabels we need
os_data = OsDataFetcher("../Projekt-OS/Data/athlete_events.csv", "Name")
ita_os_data = os_data.os_filtered_dataframe("NOC", "ITA")

app = dash.Dash(__name__)
# Dicts for funktionality of dashboard
# Dicts for filtering dataframe 

app.layout = html.Div([])


def drawing_graph():
    # Graph function needs to have abilty to draw diffrent kinds of graphs
    pass


# Data to visualize for italy 
def most_medals_per_sport():
    pass

def number_of_medals_per_os():
    pass

def another_data_function():
    pass

# Sports stats data to visualize for 2-4 sports
def age_spread_in_the_sports():
    pass

def medla_spread_for_countrys_in_sport():
    pass

def another_data_function():
    pass





if __name__ == '__main__':
    app.run_server(debug=True)
