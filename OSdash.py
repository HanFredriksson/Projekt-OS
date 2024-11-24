from FetchOSData import OsDataFetcher
import dash
import pandas as pd
import plotly.express as px 
from dash import dcc, html, Output, Input
import plotly.graph_objects as go
from plotly.subplots import make_subplots



os_data = OsDataFetcher("../Projekt-OS/Data/athlete_events.csv", "Name")

picker = {"Italy": "Italy", "Sports": "Sports"}
medals = {"Gold":"Gold", "Silver": "Silver", "Bronze": "Bronze", "Total": "Total"}

ita_filters = {"Total medals over the years": "Year", 
               "Total medals per sport": "Sport", 
               "Medals per Olympics": "City",
               "Medals for each gender per sport": "Sex"}

sport_filters ={"Age spread": "Age",
                "Medal spread per country": "NOC",
                "Gender spread": "Sex",
                "Medal distribution by gender for each sport":"genderpersport"}

graf_titel_names = {"Year": "All Olympics",
                    "Summer": "Summer Olympics",
                    "Winter": "Winter Olympics"}

sports = {"Swimming":"Swimming", 
          "Alpine Skiing":"Alpine Skiing", 
          "Rowing": "Rowing", 
          "Cross Country Skiing": "Cross Country Skiing"}

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("OS Data Analyser",style={'textAlign':'center'}),
    html.Div([

        html.Label("What category to look into:", style={"width": "200px", "display": "inline-block"}),
        dcc.Dropdown(
            id="ita-or-sports", 
            options=[{"label": k, "value": v} for k, v in picker.items()], 
            value="Italy",
            style={"width": "100px"},
            clearable= False
        ),
        

        html.Div(
            id="sport-selector", 
            style={"display": "none"}, 
            children=[
                html.Label("Choose a sport:"),
                dcc.Dropdown(
                    id="sport-picker", 
                    options=[{"label": sport, "value": sport} for sport in sports], 
                    value="Swimming",
                    clearable= False
                ),
                html.Label("Choose a filter:"),
                dcc.Dropdown(
                    id="filter-sport", 
                    options=[{"label": key, "value": value} for key, value in sport_filters.items()], 
                    value="Age",
                    clearable= False
                )
            ]
        ),
      

        

        html.Div(
            id="italy-selecter", 
            children=[
                html.Label("Select filter:", style={"width": "250px", "display": "inline-block"}), 
              dcc.Dropdown(
                    id="italy-medals", 
                    options=[{"label": key, "value": value} for key, value in ita_filters.items()], 
                    value="Year",
                    style={"width": "250px"},
                    clearable= False
                ),
            ]),
        html.Div(
            id="season-medals-container",
            children=[
                html.Label("Medals:"),
                dcc.Dropdown(
                    id="season-medals", 
                    options=[
                        {"label": "All Olympics", "value": "Year"},
                        {"label": "Summer Olympics", "value": "Summer"},
                        {"label": "Winter", "value": "Winter"}
                    ],
                    value="",
                    style={"width": "160px"}
                )
            ], style={"display": "none"}
        )
    ]),


    html.H4(),
    dcc.Graph(id="graph")
],
                      style={'background-image':'url("/assets/os.jpg")',
                             'background-size': 'cover', 
                             'position':'fixed',
                             'width':'100%',
                             'height':'100%'
                             })


@app.callback(
        [
        Output("sport-selector", "style"),
        Output("italy-selecter", "style"),
        Output("season-medals-container", "style"),
        ],
        [
        Input("ita-or-sports", "value"),
        Input("italy-medals", "value")
        ]
)

def show_or_hide (selection1, selection2):
    if selection1 == "Sports":
        return {"display": "block"}, {"display": "none"}, {"display": "none"}
    elif selection1 == "Italy":
        if selection2 == "Year":
            return{"display": "none"}, {"display": "block"}, {"display": "block"}
        else:
            return{"display": "none"}, {"display": "block"}, {"display": "none"}
    


@app.callback(
    Output("graph", "figure"),
    [
    Input("ita-or-sports", "value"),
    Input("sport-picker", "value"),
    Input("filter-sport", "value"),
    Input("italy-medals", "value"),
    Input("season-medals", "value")
    ]
)
def show_graf(cat, sport, sport_filter, italy_filter, os_season):
    """
    param data: data frame to plot
    peram cat: the span of the data
    peram graf: type of graf "bar", "line", "histo"
    """

    if cat == "Sports":
        
        
        if sport_filter == "genderpersport": 
            df= medal_counter("Sport", sport, "Sex")
            df.reset_index(inplace=True)
            fig= px.bar(df, x= "Sex", y =["Gold medals", "Silver medals", "Bronze medals"],
            barmode="stack", title=f"Medals for each gendr in {sport}",
            color_discrete_map={
            "Gold medals":"gold",
            "Silver medals":"silver",
            "Bronze medals":"chocolate"
            })
        else:
          df = medal_counter("Sport", sport, sport_filter)
          fig = px.histogram(df, x=df.index, y= "Total")
        
        if sport_filter == "Sex":
         fig = px.bar(df, x= df.index,y= "Total", color="Sex", barmode="group")
    
            
     
    elif cat == "Italy":
        df = medal_counter("NOC", "ITA", italy_filter)
        
        if os_season == "Winter" or os_season == "Summer":
            df = medal_counter("NOC", "ITA", ["Season", "Year"])
            df = df.loc[os_season]
        if os_season:
            fig = make_subplots(rows=2, cols=2, subplot_titles=["Total Medals", "Gold Medals", "Silver Medals", "Bronze Medals"])
            
            fig.add_trace(
                go.Bar(x=df.index ,y=df["Total"], name="Total Medals"),
                row=1, col=1
            )
            fig.add_trace(
                go.Bar(x=df.index, y= df["Gold medals"], name="Gold Medals"),
                row=1, col=2
            )
            fig.add_trace(
                go.Bar(x=df.index, y=df["Silver medals"], name="Silver Medals"),
                row=2, col=1
            )
            fig.add_trace(
                go.Bar(x=df.index, y=df["Bronze medals"], name="Bronze Medals"),
                row=2, col=2
            )
            fig.update_layout(title_text=f"Medels for {graf_titel_names[os_season]}")
        
        if italy_filter == "Sex":
            fig = px.bar(df, x=df.index, y= "Total", color="Sex")
        else:
             fig = px.bar(df, x=df.index, y= "Total",)
        
    fig.update_layout(
        paper_bgcolor='rgb(255,255,255,0)', 
        plot_bgcolor='rgb(255,255,255,0.9)')
    fig.update_xaxes(title_font={"color": "rgb(0,0,0,0)"}, tickfont={"color": "black"}) # source chatgpt
    fig.update_yaxes(title_font={"color": "black"}, tickfont={"color": "black"}) # source chatgpt
    
    return fig
   

  


def avreges(pick, filter, count_in):
    
    medal_data = medal_counter(pick, filter, count_in)

    avg_medals = (
        medal_data.groupby(medal_data.index)["Total"].mean()
        .reset_index()
        .rename(columns={"Total": "Average Medals"})
    )

    return avg_medals


    

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
    
    if  count_in == ["Sport", "Sex"]:
        medal_count.reset_index(inplace=True)
        medal_count.set_index(count_in[0], inplace= True)
    
    return medal_count




if __name__ == '__main__':
    app.run_server(debug=True)
