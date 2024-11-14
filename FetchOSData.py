import pandas as pd


class OsDataFetcher:

    def __init__(self, file_path):
        """ Loads data from path. Functions to make filtered dataframes and save as csv file
        """
        self._path = file_path
        self.data = pd.read_csv(file_path)


    def os_filtered_dataframe(self, col, filter):
        """Retruns filtered a dataframe\n
        col: Column to filter from\n
        filter: What you want to filter out from rows\n
        return: A filterd pandas dataframe\n
        """

        df = self.data[self.data[col] == filter]

        return  df
    
    def os_data_saver(self, name, data): 
        """Save file as CSV in the original files path\n
        name: str - Name the file\n
        data: pd.df - Wich pandas dataframe to save\n
        """
        filepath = self._path.parent / f"{name}.csv"  

        filepath.parent.mkdir(parents=True, exist_ok=True)  

        data.to_csv(filepath)  