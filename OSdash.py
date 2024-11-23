from FetchOSData import OsDataFetcher
import dash
import pandas as pd
import plotly.express as px 
from dash import dcc, html, Output, Input
import plotly.graph_objects as go



os_data = OsDataFetcher("../Projekt-OS/Data/athlete_events.csv", "Name")

picker = {"Italy": "Italy", "Sports": "Sports"}
medals = {"Gold":"", "Silver": "Silver", "Bronze": "Bronze", "Total": "Total"}

ita_filters = {"Total medals over the years": "Year", 
               "Total medals per sport": "Sport", 
               "Medals per Olympics": "City",
               "Medals for each gender per sport": "Sex"}

sport_filters ={"Age spread": "Age",
                "Medal spread per country": "NOC",
                "Gender spread": "Sex"}

sports = {"Swimming":"Swimming", "Alpine Skiing":"Alpine Skiing", "Rowing": "Rowing", "Cross Country Skiing": "Cross Country Skiing"}

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("OS Data Analyser"),
    html.Div([
        html.Label("What catogory too look into:"),
        dcc.RadioItems(id="ita-or-sports", options=picker, value="Italy")
    ]),
    html.Div(
        id = "sport-selector", 
        style = {"display": "none"},
        children=[
            html.Label("Choose a sport:"),
            dcc.RadioItems(id="sport-picker", 
                           options=[{"label": sport, "value": sport} for sport in sports], 
                           value="Swimming"),

            html.Label("Choose a filter:"),
            dcc.RadioItems(id="filter-sport", 
                           options=[{"label": key, "value": value} for key, value in sport_filters.items()], 
                           value="Age"),
                           
    ]),
    html.Div(id ="italy-selecter", children=[
            html.Label("Select filter:"), 
            dcc.RadioItems(id="italy-medals", 
                           options=[{"label": key, "value": value} for key, value in ita_filters.items()], 
                           value="Year")
    ]),
    dcc.Graph(id="graph1"),
    dcc.Graph(id="graph2"),
    dcc.Graph(id="graph3")
])

@app.callback(
        Output("sport-selector", "style"),
        Output("italy-selecter", "style"),
        Input("ita-or-sports", "value")
)

def sport_picker_show(selected_sport):
    if selected_sport == "Sports":
        return{"display": "block"}, {"display": "none"}
    if selected_sport == "Italy":
        return{"display": "none"}, {"display": "block"}


@app.callback(
    [
    Output("graph1", "figure"),
    Output("graph2", "figure")
    ],
    [
    Input("ita-or-sports", "value"),
    Input("sport-picker", "value"),
    Input("filter-sport", "value"),
    Input("italy-medals", "value")
    ]
)
def show_graf(cat, sport, sport_filter, italy_filter):
    """
    param data: data frame to plot
    peram cat: the span of the data
    peram graf: type of graf "bar", "line", "histo"
    """
    if cat == "Sports":
        df = medal_counter("Sport", sport, sport_filter)
        fig1 = px.histogram(df, x=df.index, y= "Total")
        return fig1, {}
      
    elif cat == "Italy":
        df = medal_counter("NOC", "ITA", italy_filter)
        fig1 = px.bar(df, x=df.index, y= "Total")
        fig2 = px.bar(df, x=df.index, y= "Gold medals")
        return fig1, fig2
    # kolla på subplots
  


def avreges(pick, filter, count_in):
    
    medal_data = medal_counter(pick, filter, count_in)

    avg_medals = (
        medal_data.groupby(medal_data.index)["Total"].mean()
        .reset_index()
        .rename(columns={"Total": "Average Medals"})
    )

    return avg_medals

@app.callback(
     Output("graph3", "figure"),
     Input("sport-picker", "value")
     )
  
def gender_distr_sport(sport):
    
    df = medal_counter(pick="Sport", filter=sport, count_in="Sex")
    
    df['Sex'] = df['Sex'].map({'M':'Male', 'F':'Female'})
    fig3 = px.bar(df, x='Sex', 
                  y= ["Gold medals", "Silver medals", "Bronze medals"], 
                  barmode='stack', 
                  title=f"Medal Distribution by gender in {sport}",
                  color_discrete_map={
                      "Gold medals": "gold",
                      "Silver medlas": "silver", 
                      "Bronze medlas": "chocolate-colored"
                  })
    return fig3

    

def medal_counter(pick, filter, count_in):
    """Counts the medals from picked country or sport from
    a grouped column. 
    Retruns a data frame with total and each variation of medal 
    with count_in as index

    param pick: are sport or country
    param filter: Wich sport or country
    param count_in: For wich columne to count medals

    """
    dff = os_data.os_filtered_dataframe(pick, filter)

    if count_in == "Sex":
        count_in = ["Sport", "Sex"]

    gold_medal = dff[dff["Medal"] == "Gold"].groupby(count_in).size()
    silver_medal = dff[dff["Medal"] == "Silver"].groupby(count_in).size()
    bronze_medal = dff[dff["Medal"] == "Bronze"].groupby(count_in).size()

    medal_count = pd.DataFrame({"Gold medals": gold_medal,
                                "Silver medals": silver_medal,
                                "Bronze medals": bronze_medal,
                                }).fillna(0).astype(int).reindex()
    
    medal_count["Total"] = medal_count["Gold medals"] + medal_count["Silver medals"] + medal_count["Bronze medals"]
    
    if count_in == ["Sport", "Sex"]:
        medal_count.reset_index(inplace=True)
        medal_count.set_index("Sport", inplace= True)
    
    return medal_count




if __name__ == '__main__':
    app.run_server(debug=True)
