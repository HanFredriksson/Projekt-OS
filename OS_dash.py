from FetchOSData import OsDataFetcher

os_data = OsDataFetcher("../Projekt-OS/Data/athlete_events.csv", "Name")

ita_os_data = os_data.os_filtered_dataframe("NOC", "ITA")