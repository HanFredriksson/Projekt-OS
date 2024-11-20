from FetchOSData import OsDataFetcher
import dash

# The variabels we need
os_data = OsDataFetcher("../Projekt-OS/Data/athlete_events.csv", "Name")
ita_os_data = os_data.os_filtered_dataframe("NOC", "ITA")

app = dash.Dash(__name__)
# Dicts with key for what we want to filter for showing in the graphs.
# Keys get picked from a meny in dashboard
# Do we need to move the filter function from the class?
# Or filter funktion of the class is a general filter making smaller dataframes, like one for each sport
# 

app.layout = html.Div([])


def drawing_graph():
    # Graph function needs to have abilty to draw diffrent kinds of graphs
    # Graphs needed: Histogram, Pie chart, Line chart, box chart
    pass


def calc_averge():
    # Calculate on averag how many medals in each denomination each genader has gotten
    pass

# Data to visualize for italy 
def medals_per_year():
    # How succsesfull italy has been over the years
    # Possibley show by medal typ and/or winter or summer olympices
    pass

def most_medals_per_sport():
    # How many medals through out the year have Italy taken in
    # Possibley see wich medal type
    pass

def number_of_medals_per_os():
    # Show how the medals where spread over the diffrent Olympices
    pass

def gender_distrbution_sport():
    # Comparing an average over won medals devided in medal denomination
    pass


# Sports stats data to visualize for 2-4 sports: Swimming, Alpine Skiing, Rowing, Cross Country Skiing
def age_spread_in_the_sports(sport):
# Show how the medals spread over the ages in the sport
    sport_df = os_data.os_filtered_dataframe("Sport", sport)
    madal_age = sport_df.groupby("Age")["Medal"].count().reset_index()
    madal_age.columns = ["Age", "Medal Count"]
    
    return madal_age
    

def medal_spread_for_countries_in_sport():
    # Show how the medals spread over the countries in the sport
    pass

def gender_distrbution_sports():
    # Comparing an average over won medals up in medal denomination
    pass





if __name__ == '__main__':
    app.run_server(debug=True)
