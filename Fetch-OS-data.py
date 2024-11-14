import pandas as pd
from pathlib import Path  
class OsDataFetcher:

    
# Load file and filter
os_data = pd.read_csv("../Projekt-OS/Data/athlete_events.csv")

italy_os_data = os_data[os_data["NOC"] == "ITA"]


  
# Save file as CSV with filter
filepath = Path("../Projekt-OS/Data/Italy-OS-data.csv")  

filepath.parent.mkdir(parents=True, exist_ok=True)  

italy_os_data.to_csv(filepath)  