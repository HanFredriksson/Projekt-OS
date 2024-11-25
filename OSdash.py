from FetchOSData import OsDataFetcher
import dash
import pandas as pd
import plotly.express as px 
from dash import dcc, html, Output, Input
import plotly.graph_objects as go
from plotly.subplots import make_subplots



os_data = OsDataFetcher("../Projekt-OS/Data/athlete_events.csv", "Name")

picker = {"Italy": "Italy", "Sports": "Sports"}
ita_filters = {"Total medals over the years": "Year", 
               "Total medals per sport": "Sport", 
               "Medals per Olympics": "City",
               "Medals for each gender per sport": "Sex"}

sport_filters ={"Age spread": "Age",
                "Medal spread per country": "NOC",
                "Gender participation over time": "gender_participation",
                "Medal distribution by gender for each sport":"genderpersport",
                
                }

graf_titel_names = {"Year": "All Olympics",
                    "Summer": "Summer Olympics",
                    "Winter": "Winter Olympics",
                    }

sports = {"Swimming":"Swimming", 
          "Alpine Skiing":"Alpine Skiing", 
          "Rowing": "Rowing", 
          "Cross Country Skiing": "Cross Country Skiing"}

color_map = {"Gold medals":"gold",
            "Silver medals":"silver",
            "Bronze medals":"chocolate",
            "Average Medals": "deepskyblue",
            "Averages_sex" : "Sex",
            "Year": "Total",
            "Sport": "Total",
            "City": "Total",
            "Sex" : "Sex"
            } 

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("OS Data Analyser",style={'textAlign':'center'}),
    html.Div([

        html.Label("Select a category:", style={"width": "200px", "display": "inline-block"}),
        dcc.Dropdown(
            id="ita-or-sports", 
            options=[{"label": k, "value": v} for k, v in picker.items()], 
            value="Italy",
            style={"width": "100px", "margin-bottom": "10px"},
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
                    style={"width": "180px", "margin-bottom": "10px"},
                    clearable= False
                ),
                html.Label("Choose a filter:"),
                dcc.Dropdown(
                    id="filter-sport", 
                    options=[{"label": key, "value": value} for key, value in sport_filters.items()], 
                    value="Age",
                    style={"width": "250px"},
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
                    style={"width": "250px", "margin-bottom": "10px"},
                    clearable= False
                ),
                html.Label("Medals per gender:",
                style={"display": "none"}),
                dcc.RadioItems(
                    id="gender-medals",
                    options=[
                        {"label": "Total Medals", "value": "Total"},
                        {"label": "Average Medals", "value": "Averages_sex"},
                    ],
                    value="Total",
                    
                )
            ]
            ),


        html.Div(
            id="season-medals-container",
            children=[
                html.Label("Medals:"),
                dcc.Dropdown(
                    id="season-medals", 
                    options=[
                        {"label": "All Olympics", "value": "Year"},
                        {"label": "Summer Olympics", "value": "Summer"},
                        {"label": "Winter Olympics", "value": "Winter"}
                    ],
                    value="",
                    style={"width": "160px"}
                )
            ]
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
        Output("gender-medals", "style"),
        Output("season-medals-container", "style"),
        Output("season-medals", "value"),
    ],
    [
        Input("ita-or-sports", "value"),
        Input("italy-medals", "value")
    ]
)
def show_or_hide(selection1, selection2):
    if selection1 == "Sports":
        # Visa sportval, göm alla andra
        return {"display": "block"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, "Year"  
    
    elif selection1 == "Italy":
        # Kontrollera vilket filter som valts i italy-medals
        if selection2 == "Sex":
            # Visa Average Medals
            return {"display": "none"}, {"display": "block"}, {"display": "block"}, {"display": "none"}, ""  
        elif selection2 == "Year":
            # Visa Medals-dropdown
            return {"display": "none"}, {"display": "block"}, {"display": "none"}, {"display": "block"},""
        else:
            # Standard: Visa bara Italy-selecter
            return {"display": "none"}, {"display": "block"}, {"display": "none"}, {"display": "none"}, "" 
    


@app.callback(
    Output("graph", "figure"),
    [
    Input("ita-or-sports", "value"),
    Input("sport-picker", "value"),
    Input("filter-sport", "value"),
    Input("italy-medals", "value"),
    Input("season-medals", "value"),
    Input("gender-medals", "value")
    ]
)
def show_graf(cat, sport, sport_filter, italy_filter, os_season, gender_medals):


    if cat == "Sports":
        
        if sport_filter == "genderpersport": 
            df= medal_counter("Sport", sport, "Sex")
            df.reset_index(inplace=True)
            fig= px.bar(df, x= "Sex", y =["Gold medals", "Silver medals", "Bronze medals"],
            barmode="stack", title=f"Medals for each gender in {sport}",
            color_discrete_map={
            "Gold medals":"gold",
            "Silver medals":"silver",
            "Bronze medals":"chocolate"
            })
        elif sport_filter == "gender_participation":
            df = gender_participation(os_data.os_filtered_dataframe("Sport", sport), "Year")
            fig = px.line(df, x="Year", y="Count", color="Sex",
                          title=f"Gender Participation Over Time in {sport}")
        else:
            df = medal_counter("Sport", sport, sport_filter)
            if sport_filter == "NOC":
                df = df[df.values.sum(axis=1) > 5]
                df.sort_values(by="Total", ascending=True, inplace=True)
            fig = px.bar(df, x=df.index, y="Total", title=f"Medals in {sport}")

            
     
    elif cat == "Italy":
        df = medal_counter("NOC", "ITA", italy_filter)
        
        if os_season == "Winter" or os_season == "Summer":
            df = medal_counter("NOC", "ITA", ["Season", "Year"])
            df = df.loc[os_season]
        if os_season:
            fig = make_subplots(rows=2, 
                                cols=2, 
                                subplot_titles=["Total Medals", "Gold Medals", "Silver Medals", "Bronze Medals"],
                                )
            
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
            fig.update_layout(title_text=f"Medals for {graf_titel_names[os_season]}")
        
        elif gender_medals == "Averages_sex" and italy_filter == "Sex":
            
            df_gender_participation = gender_participation(os_data.os_filtered_dataframe("NOC", "ITA"), "Sport", True)
            df = averages(df, italy_filter)
            df.sort_values(by="Sport", inplace=True)
            df_gender_participation.sort_values(by="Sport", inplace=True)
            df = df.merge(df_gender_participation, on=["Sport", "Sex"], how="inner")
            
            
          
            bar_trace = go.Bar(
                x=df['Sport'],
                y=df['Average Medals'],
                name='Average Medals',
                marker_color=df['Sex'].map({'F': 'deepskyblue', 'M': 'tomato'}),
                text=df['Sex'],  # Display gender on hover
                hoverinfo="text+y"
            )

            # Line trace for Gender Participation
            line_trace = go.Scatter(
                x=df['Sport'],  
                y=df['Count'],
                name='Gender Participation',
                mode='lines+markers',
                line=dict(color='palegreen', width=3),
            )

            # Combine traces into a single figure
            fig = go.Figure(data=[bar_trace, line_trace])

            # Update layout for clarity
            fig.update_layout(
                title="Average Medals and Gender Participation",
                xaxis_title="Sport",
                yaxis_title="Average Medals",
                barmode='group'  # Group bars by gender
            )
        else:
             fig = px.bar(df, 
                          x=df.index, 
                          y= "Total", 
                          color=color_map[italy_filter],
                          title=f"Total medals over the {italy_filter}")
             
    return fig
   

  


def averages(data, group):
    
    avg_data = (
    data.groupby([group, "Sport"])[["Gold medals", "Silver medals", "Bronze medals", "Total"]].mean()
    .reset_index()
    .rename(columns={"Total": "Average Medals"}) 
    )
    move_column = avg_data.pop("Average Medals")
    avg_data.insert(0, "Average Medals", move_column)

    # # Sorting dataframe for most medels on avrage 
    # sport_totals = avg_data.groupby('Sport')['Average Medals'].sum().reset_index()
    # sport_totals = sport_totals.rename(columns={'Average Medals': 'Sport Total Medals'})

    # # Reconnect data to orignal data 
    # avg_data = avg_data.merge(sport_totals, on='Sport')

    # # Sort after total number of averages over gendr and sport
    # sorted_df = avg_data.sort_values(by=['Sport Total Medals', 'Average Medals'], 
    #                                  ascending=[False, False],)
    return avg_data

def gender_participation(data, group,medal_sports= False):
    print(data)
    if medal_sports:
        
        data = data[data["Medal"].notna()]
        
  

    participation = data.groupby([group, "Sex"]).size().reset_index(name="Count")

    return participation
    


def medal_counter(pick, filter, count_in):
    dff = os_data.os_filtered_dataframe(pick, filter)

    if count_in == "Sex":
         count_in = ["Sport", "Sex"]

    medal_types = ["Gold", "Silver", "Bronze"]
    medal_counts = {
        f"{medal} medals": dff[dff["Medal"] == medal].groupby(count_in).size()
        for medal in medal_types
    }
    medal_count = pd.DataFrame(medal_counts).fillna(0).astype(int)
    medal_count["Total"] = medal_count.sum(axis=1)

    if  count_in == ["Sport", "Sex"]:
        medal_count.reset_index(inplace=True)
        medal_count.set_index(count_in[0], inplace= True)

    return medal_count


if __name__ == '__main__':
    app.run_server(debug=True)
